import cv2
import numpy as np
import open3d as o3d

class Reconstruct3D:
    def __init__(self):
        self.orb = cv2.ORB_create()  # Feature extractor
        self.bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    def capture_images(self, num_images=10):
        """Captures multiple images from the webcam for 3D reconstruction"""
        cap = cv2.VideoCapture(0)
        images = []

        for i in range(num_images):
            ret, frame = cap.read()
            if not ret:
                break
            images.append(frame)
            cv2.imshow("Capturing Images", frame)
            cv2.waitKey(500)  # Wait 500ms between captures

        cap.release()
        cv2.destroyAllWindows()
        return images

    def compute_depth_map(self, img1, img2):
        """Compute depth map using Stereo Matching"""
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        stereo = cv2.StereoBM_create(numDisparities=64, blockSize=15)
        disparity = stereo.compute(gray1, gray2)

        depth_map = cv2.normalize(disparity, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
        depth_map = np.uint8(depth_map)

        return depth_map

    def generate_point_cloud(self, depth_map, img):
        """Generate a 3D point cloud from the depth map"""
        h, w = depth_map.shape
        fx = fy = 800  # Focal length
        cx, cy = w // 2, h // 2  # Optical center

        points = []
        colors = []

        for v in range(h):
            for u in range(w):
                depth = depth_map[v, u]
                if depth > 0:
                    x = (u - cx) * depth / fx
                    y = (v - cy) * depth / fy
                    z = depth
                    points.append((x, y, z))
                    colors.append(img[v, u] / 255.0)

        point_cloud = o3d.geometry.PointCloud()
        point_cloud.points = o3d.utility.Vector3dVector(np.array(points))
        point_cloud.colors = o3d.utility.Vector3dVector(np.array(colors))
        return point_cloud

    def save_point_cloud(self, point_cloud, filename="output.ply"):
        """Save the generated point cloud to a file"""
        o3d.io.write_point_cloud(filename, point_cloud)
        print(f"✅ 3D Model saved as {filename}")

    def run(self):
        """Main function to capture images, compute depth, and generate 3D model"""
        print("📸 Capturing images...")
        images = self.capture_images()

        if len(images) < 2:
            print("❌ Need at least two images for depth estimation!")
            return

        print("🛠️ Computing depth map...")
        depth_map = self.compute_depth_map(images[0], images[1])

        print("🔷 Generating 3D Point Cloud...")
        point_cloud = self.generate_point_cloud(depth_map, images[0])

        print("💾 Saving 3D Model...")
        self.save_point_cloud(point_cloud)

        print("🎨 Visualizing 3D Model...")
        o3d.visualization.draw_geometries([point_cloud])

if __name__ == "__main__":
    reconstructor = Reconstruct3D()
    reconstructor.run()