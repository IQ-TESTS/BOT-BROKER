import flet as ft
import json
import random
from ShareInfoParser import get_share_info



class share_card_creator:
    def __init__(self, name, image, price_dollars, change_day, prediction, confidence, new, page):
        self.name = name
        self.image = image
        self.price_dollars = price_dollars
        self.change_day = change_day
        self.prediction = prediction
        self.confidence = confidence
        self.new = new
        self.page = page

    def create_card(self):
        # Define default text based on the 'new' status
        if self.new:
            new_text = ft.Text("Recently listed in an IPO", color=ft.colors.GREEN)
        else:
            new_text = ft.Text("")

        # Check if confidence and price are integers
        confidence_text = (
            str(round(self.confidence * 100, 2)) + "%"
            if isinstance(self.confidence, (int, float))
            else "N/A"
        )

        price_text = (
            str(self.price_dollars) + "$"
            if isinstance(self.price_dollars, (int, float))
            else "N/A"
        )

        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.ListTile(
                            leading=ft.Image(src=self.image),
                            title=ft.Text(self.name),
                            subtitle=new_text
                        ),
                        ft.Row(
                            [
                                ft.Text("Prediction: " + self.prediction),
                                ft.Text("Confidence: " + confidence_text),
                                ft.Text("Price: " + price_text),
                                self.change_text()
                            ],
                            alignment=ft.MainAxisAlignment.END,
                        ),
                    ]
                ),
                height=115,
                width=self.page.window.width + 200,
                padding=10,
            )
        )

    def change_text(self):
        try:
            if(self.change_day < 0):
                return ft.Text(str(self.change_day) + "%", color=ft.colors.RED)
            elif(self.change_day == 0):
                return ft.Text("+" + str(self.change_day) + "%", color=ft.colors.ORANGE)
            else:
                return ft.Text("+" + str(self.change_day) + "%", color=ft.colors.GREEN)
        except:
            return ft.Text("+/- N/A")

class get_json:
    def __init__(self, json_name):
        self.json_name = json_name

    def load_json(self):
        with open("assets/" + self.json_name + ".json", "r") as file:
            data = json.load(file)
        return data

async def main(page: ft.Page):
    # Настройки приложения по умолчанию
    page.title = "BotBroker"
    page.theme_mode = "dark"
    page.window.full_screen = True

    page.window.width = 900
    page.window.height = 650


    page.on_resize = lambda _: page.update()

    page.fonts = {
        "LemonMilkBold": "fonts/LemonMilkBold.otf",
    }

    ensure_data()

    async def route_change(route):
        page.views.clear()

        # Приветственная страница
        if page.route == "/home":
            data = get_json("shares_list")

            shares_list = ft.Column(
                controls=[],
                expand=True,
                scroll=ft.ScrollMode.AUTO
            )

            shares_data = data.load_json().get("shares", [])

            # Separate valid and invalid shares
            valid_shares = []
            no_data_shares = []

            for share in shares_data:
                if isinstance(share.get("confidence"), (int, float)) and isinstance(share.get("price_dollars"),
                                                                                    (int, float)):
                    valid_shares.append(share)
                else:
                    no_data_shares.append(share)
                    print("Invalid share data:", share)

            # Sort the valid shares by confidence in descending order
            sorted_shares = sorted(valid_shares, key=lambda x: x.get("confidence", 0), reverse=True)

            # Create cards for sorted shares
            for share in sorted_shares:
                scc = share_card_creator(
                    share.get("name"),
                    share.get("image"),
                    share.get("price_dollars"),
                    share.get("change_day"),
                    share.get("prediction"),
                    share.get("confidence"),
                    share.get("new"),
                    page
                )
                shares_list.controls.append(scc.create_card())

            # Optionally, you can display cards for no_data_shares separately if needed
            for share in no_data_shares:
                scc = share_card_creator(
                    share.get("name"),
                    share.get("image"),
                    share.get("price_dollars"),
                    share.get("change_day"),
                    share.get("prediction"),
                    share.get("confidence"),
                    share.get("new"),
                    page
                )
                shares_list.controls.append(scc.create_card())

            # Add the sorted share cards to the view
            page.views.append(
                ft.View(
                    route='/home',
                    controls=[
                        ft.Text("Bot Broker", font_family="LemonMilkBold", size=50),
                        ft.Text(" "),
                        shares_list,
                        ft.Card(
                            content=ft.Column(
                                controls=[
                                    ft.Row(
                                        controls=[
                                            ft.Text("Help project:", font_family="LemonMilkBold"),
                                            ft.TextButton("@botbroker_helpproject",
                                                          url="https://t.me/botbroker_helpproject")
                                        ]
                                    ),
                                    ft.Row(
                                        controls=[
                                            ft.Text("Need help?:", font_family="LemonMilkBold"),
                                            ft.TextButton("@botbroker_helpusers",
                                                          url="https://t.me/botbroker_helpusers")
                                        ]
                                    )
                                ]
                            )
                        )
                    ],
                    vertical_alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )

            page.update()

        page.update()

    # Анимация перехода между страницами
    async def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        await page.go_async(top_view.route)

    # Переход на приветственную страницу при запуске приложения
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    await page.go_async('/home')


def ensure_data():
        data = get_json("shares_list")
        loaded_data = data.load_json()

        # Iterate through each share in the loaded data
        for share in loaded_data.get("shares", []):
            try:
                ticker = share.get("ticker")  # Adjust based on your actual JSON structure
                parsed_data = get_share_info(ticker)
                print(parsed_data)

                # Update the dictionary with the new data
                share["price_dollars"] = parsed_data.get("price")
                share["change_day"] = parsed_data.get("percentage_change")

                def clamp_confidence(confidence):
                    # Ensure the confidence is between 0.05 and 9.9
                    return max(0.05, min(confidence, 9.93))

                if share.get("change_day") > 0 and share.get("change_day") <= 1:
                    share["prediction"] = "Sell"
                    confidence = round(share.get("change_day"), 2) - round(random.uniform(0.1, 0.9), 2)
                    share["confidence"] = clamp_confidence(confidence)

                elif share.get("change_day") > 1:
                    share["prediction"] = "Sell"
                    confidence = 1 - round(random.uniform(0.1, 2.9), 2)
                    share["confidence"] = clamp_confidence(confidence)

                elif share.get("change_day") < 0 and share.get("change_day") >= -1:
                    share["prediction"] = "Buy"
                    confidence = round(share.get("change_day") * -1, 2) - round(random.uniform(0.1, 0.9), 2)
                    share["confidence"] = clamp_confidence(confidence)

                elif share.get("change_day") < -1:
                    share["prediction"] = "Buy"
                    confidence = 1 - round(random.uniform(0.1, 0.9), 2)
                    share["confidence"] = clamp_confidence(confidence)

                else:
                    share["prediction"] = "Keep"
                    share["confidence"] = 1

                # Save the updated data back to the JSON file (if needed)
                with open("assets/shares_list.json", "w") as file:
                    json.dump(loaded_data, file, indent=4)

            except:
                share["prediction"] = "N/A"
                share["confidence"] = "N/A"
                with open("assets/shares_list.json", "w") as file:
                    json.dump(loaded_data, file, indent=4)


# Run Flet app in the main thread
if __name__ == "__main__":
    # Run Flet app in the main thread
    ft.app(target=main, assets_dir='assets', view=ft.AppView.WEB_BROWSER)