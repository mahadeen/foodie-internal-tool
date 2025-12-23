import argparse
from pathlib import Path
import json

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", type=str)
    args = parser.parse_args()
    file_path = Path(args.input_path)

    if not file_path.exists() or not file_path.is_file():
        print(f"File does not exist: {file_path}")
        return
    text = file_path.read_text()
        
    try:
        data = json.loads(text)
    except Exception as e:
        print("Error parsing JSON")
        return
    
    orders = data.get('orders', [])
    report = get_report (orders)
    json_report = json.dumps(report, indent=4)

    output_file = open('output.json', 'w')
    output_file.write(json_report)
    output_file.close()

def get_report(orders):
    result = {
        'count': orders_count(orders),
        'avg order value': avg_order_value(orders),
        'avg daily order count': avg_daily_order_count(orders),
        'avg hourly revenue': avg_hourly_revenue(orders),
        'completion rate': completion_rate(orders),
        'top_2_restaurants': top_performing_restaurants(orders),
        'least_2_restaurants': least_performing_restaurants(orders),
    }
    return result

def orders_count (orders):
    count = len(orders)
    return count

def avg_order_value (orders):
    if not orders:
        return 0
    # get avg total value of orders
    total = sum(order['total'] for order in orders)
    # get number of orders
    count = orders_count(orders)
    # divide total value by number of orders
    avg = total / count
    return round(avg, 2)

def avg_daily_order_count (orders):
    # get total number of orders
    count = orders_count (orders)
    # devide count by 7 days (assuming that it's a weekly report)
    daily_avg_count = count / 7
    return round(daily_avg_count, 2)

def avg_hourly_revenue (orders):
    # get total orders value
    total = sum(order['total'] for order in orders)
    # devide total by 168 (24 hours * 7 days) (assuming that it's a weekly report)
    avg_hourly_revenue = total / 168
    return round(avg_hourly_revenue, 2)

def completion_rate(orders):
    if not orders:
        return "0 %"
    # count completed orders by iterating through dict
    count = 0
    for order in orders:
        value = order['status']
        if value == "completed":
            count = count + 1
    # calculate percentage
    percentage = count / orders_count(orders)
    return f'{int(percentage * 100)} %'
        
def group_values (orders):
    # create an empty array
    grouped = {}
    # iterate through the dict
    for order in orders:
        res_id = order['restaurant_id']
        res_name = order ['restaurant_name']
        total = order ['total']

        # check if the restaurant doesn't exist in the new array
        if res_id not in grouped:
            grouped[res_id] = {
                'restaurant_id': res_id,
                'restaurant_name': res_name,
                'total_revenue': total,
                'orders_count': 1,
            }
        else:
            # append only the value to that
            grouped[res_id]['total_revenue'] += total
            grouped[res_id]['orders_count'] += 1

    return list(grouped.values())

def by_total_revenue(item):
    return item['total_revenue']

def top_performing_restaurants(orders):
    grouped = group_values(orders)
    grouped.sort(key=by_total_revenue, reverse=True)
    return grouped[:2]


def least_performing_restaurants(orders):
    grouped = group_values(orders)
    grouped.sort(key=by_total_revenue)
    return grouped[:2]

if __name__ == "__main__":
    main()