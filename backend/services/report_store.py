class ReportStore:
    def __init__(self):
        self.latest_result = None

    def set_result(self,result: dict):
        self.latest_result = result

    def get_result(self):
        return self.latest_result

    def clear(self):
        self.latest_result = None

report_store = ReportStore()