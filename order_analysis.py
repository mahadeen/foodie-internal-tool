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
        'avg_order_value': avg_order_value(orders)
    }
    return result


def orders_count (orders):
    count = len(orders)
    return count

def avg_order_value (orders):
    total = sum(order['total'] for order in orders)
    count = orders_count(orders)
    avg = total / count
    return avg

# def mean_daily_order_count (request):
#     # orders_count () devided by 7 (days)
#     # return value
#     return

# def mean_hourly_revenue (request):
#     # mean_order_value () devided by 24 hours
#     # return value
#     return

# def top_performing_restaurants(request):
#     # retrieve all orders
#     # match them by restaurants
#     # get the "max" value of orders for the top 5 restaurants
#     # return values
#     return

# def least_performing_restaurants(request):
#     # retrieve all orders
#     # match them by restaurants
#     # get the "min" value of orders for the top 5 restaurants
#     # return values
#     return

# def completion_rate(request):
#     # retrieve all orders
#     # match them by statuses
#     # return value
#     return

if __name__ == "__main__":
    main()