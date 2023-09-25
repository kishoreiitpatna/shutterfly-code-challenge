from collections import defaultdict
from datetime import datetime, timedelta

class CustomerLTVCalculator:
    def __init__(self):
        self.customer_data = defaultdict(list)
        self.week_start = {}

    def ingest(self, event):
        event_type = event['type']
        if event_type == 'CUSTOMER':
            self._handle_customer_event(event)
        elif event_type == 'SITE_VISIT':
            self._handle_site_visit_event(event)
        elif event_type == 'ORDER':
            self._handle_order_event(event)
        elif event_type == 'IMAGE':
            self._handle_image_upload_event(event)

    def _handle_customer_event(self, event):
        customer_id = event['key']
        self.customer_data[customer_id].append(event)

    def _handle_site_visit_event(self, event):
        customer_id = event['customer_id']
        self.customer_data[customer_id].append(event)

    def _handle_order_event(self, event):
        customer_id = event['customer_id']
        self.customer_data[customer_id].append(event)

    def _handle_image_upload_event(self, event):
        customer_id = event['customer_id']
        self.customer_data[customer_id].append(event)

    def calculate_ltv(self, customer_id, average_lifespan=10):
        if customer_id not in self.customer_data:
            return 0

        customer_events = self.customer_data[customer_id]
        order_total = sum(event['total_amount'] for event in customer_events if event['type'] == 'ORDER')

        if not order_total:
            return 0

        # Extract all 'ORDER' event times across all customers
        all_order_event_times = [event['event_time'] for events in self.customer_data.values() for event in events if event['type'] == 'ORDER']

        if not all_order_event_times:
            return 0

        # Calculate the duration in weeks from the first usage time of the specific customer
        first_event_time = min(event['event_time'] for event in customer_events)
        last_event_time = max(all_order_event_times)

        event_duration_weeks = self._calculate_weeks(first_event_time, last_event_time)

        if event_duration_weeks == 0:
            return 0

        average_weekly_spend = order_total / event_duration_weeks
        ltv = average_weekly_spend * average_lifespan * 52
        return ltv

    def top_x_simple_ltv_customers(self, x):
        ltv_values = [(customer_id, self.calculate_ltv(customer_id)) for customer_id in self.customer_data]
        sorted_ltv_values = sorted(ltv_values, key=lambda x: x[1], reverse=True)
        return sorted_ltv_values[:x]

    def _calculate_weeks(self, start_date, end_date):
        start_date = datetime.fromisoformat(start_date)
        end_date = datetime.fromisoformat(end_date)

        # Define a week as Sunday to Saturday
        days_in_week = 7
        days_to_sunday = (start_date.weekday() - 6) % days_in_week
        start_of_week = start_date - timedelta(days=days_to_sunday)
        days_to_saturday = (end_date.weekday() - 5) % days_in_week
        end_of_week = end_date + timedelta(days=days_to_saturday)

        event_duration_weeks = (end_of_week - start_of_week).days / 7
        return event_duration_weeks

# Example usage:
if __name__ == '__main__':
    calculator = CustomerLTVCalculator()
    
    # Sample event data (replace with actual data ingestion)
    events = [
        {
            'type': 'CUSTOMER',
            'key': 'customer1',
            'event_time': '2023-01-01',
            'last_name': 'Doe',
            'adr_city': 'New York',
            'adr_state': 'NY',
        },
        {
            'type': 'SITE_VISIT',
            'customer_id': 'customer1',
            'event_time': '2023-01-02',
            'page_id': 'page1',
            'tags': [{'name': 'tag1', 'value': 'value1'}],
        },
        {
            'type': 'ORDER',
            'customer_id': 'customer1',
            'event_time': '2023-01-05',
            'order_id': 'order1',
            'total_amount': 200,
        },
        {
            'type': 'CUSTOMER',
            'key': 'customer2',
            'event_time': '2023-01-03',
            'last_name': 'Smith',
            'adr_city': 'Los Angeles',
            'adr_state': 'CA',
        },
        {
            'type': 'ORDER',
            'customer_id': 'customer2',
            'event_time': '2023-01-07',
            'order_id': 'order2',
            'total_amount': 100
        },
        {
            'type': 'ORDER',
            'customer_id': 'customer2',
            'event_time': '2023-01-12',
            'order_id': 'order3',
            'total_amount': 50,
        },
    ]

    for event in events:
        calculator.ingest(event)

    top_customers = calculator.top_x_simple_ltv_customers(1)
    print(top_customers)
