from transformers import pipeline

class QueryClassifier:
    def __init__(self):
        """Initialize NLP model for text classification"""
        self.classifier = pipeline("text-classification", model="facebook/bart-large-mnli")

    def categorize(self, question):
        """Categorize query as 'Real-Time' or 'General Knowledge'"""
        categories = ["Real-Time Query", "General Knowledge Query"]
        result = self.classifier(question, candidate_labels=categories)
        return result["labels"][0]  # Return top category