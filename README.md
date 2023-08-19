# Food Saver - Expiration Tracker

Food Saver is a simple Python program designed to help you keep track of the expiration dates of your stored food items. It allows you to add food items, check their expiration status, and delete items from the database. The program also has the capability to send mobile notifications for foods that have expired.

## Getting Started

### Prerequisites

You need to have Python 3.x installed on your system. If you haven't already, you can download it from the Python official website.

### Installation

1. Clone this repository to your local machine:

```bash
git clone https://github.com/yanere/foodsaver.git
```

2. Navigate to the project directory:

```bash
cd foodsaver
```

3. Install the required package by running the following command:

```python
pip install requests
```

### Usage

1. **Important**: To enable mobile notifications, you need to create a topic in the ntfy mobile app. The program uses ntfy to send notifications.

- Go to [NTFY](https://ntfy.sh/) and download the mobile app.
- Create a new topic in the mobile app
- Open saver.py in your editor.
- Locate the send_notification function.
- Replace the URL in the requests.post line with your own ntfy topic URL.

This is how the line should look:

```python
    requests.post("https://ntfy.sh/<yourtopic>",
                  data=f"{food_name} has expired 😞".encode(encoding='utf-8'))
```

2. Run the program by executing the following command:

```bash
python saver.py
```

The program provides you with several options:

- **Add Food**: Add a new food item to the database along with its expiration date.
- **Check Expiration**: Display the expiration status of all food items.
- **Delete Food**: Remove a food item from the database.

3. Follow the on-screen prompts to use the program's features.

4. The program runs indefinitely until you manually stop it. It will also send notifications for expired food items at a daily interval.

## Contributing

Contributions are welcome! If you find any bugs, have suggestions for improvements, or want to add new features, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
