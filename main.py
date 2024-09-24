import flet as ft
import json
import random
import time
<<<<<<< HEAD
from ShareInfoParser import get_share_info, get_share_graph, predict_stock_trend
=======
from ShareInfoParser import get_share_info
>>>>>>> 27c601ff6a7dc7d643b47abbc13c7cf92fdbdbb4



class share_card_creator:
    def __init__(self, name, image, price_dollars, change_day, prediction, confidence, volume, ticker, new, page):
        self.name = name
        self.image = image
        self.price_dollars = price_dollars
        self.change_day = change_day
        self.prediction = prediction
        self.confidence = confidence
        self.volume = volume
        self.ticker = ticker
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
            str(round(self.confidence * 100, 3)) + "%"
            if isinstance(self.confidence, (int, float))
            else "N/A"
        )

        price_text = (
            str(self.price_dollars) + "$"
            if isinstance(self.price_dollars, (int, float))
            else "N/A"
        )

        volume_text = (
            str(self.volume)
            if isinstance(self.volume, (int, float))
            else "N/A"
        )

        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                                ft.ListTile(
                                    leading=ft.Image(src=self.image),
                                    title=ft.Text(self.name),
                                    subtitle=new_text,
                                ),

                                ft.Row(
                                    [
                                        ft.Text("Prediction: " + self.prediction),
                                        ft.Text("Confidence: " + confidence_text),
                                        # ft.Text("Volume: " + volume_text),
                                        ft.Text("Price: " + price_text),
                                        self.change_text(),
                                        ft.IconButton(icon=ft.icons.INFO, icon_size=20, tooltip="More", on_click=lambda _: self.page.go(f"/about:{self.ticker}")),
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


    async def route_change(route):
        page.views.clear()

        # if page.route == "/welcome":
        #     page.views.append(
        #         ft.View(
        #             route="/welcome",
        #             controls=[
        #                 ft.Text("Bot Broker", font_family="LemonMilkBold", size=50),
        #
        #                 ft.Text(" "),
        #                 ft.Text(" "),
        #
        #                 ft.Text("#1 AI POWERED BROKER", font_family="LemonMilkBold", size=30),
        #                 ft.Text(" "),
        #                 ft.Text("NEVER BEEN SO EASY", font_family="LemonMilkBold", size=30),
        #
        #                 ft.Text(" "),
        #                 ft.Text(" "),
        #
        #                 ft.ElevatedButton("USE NOW")
        #
        #
        #                 # ft.Row(
        #                 #     controls=[ft.Text("#1 AI POWERED BROKER", font_family="LemonMilkBold", size=30), ft.Image(src="AI-LOGO.png", width=400, height=400)],
        #                 #     alignment=ft.MainAxisAlignment.CENTER
        #                 # )
        #             ],
        #             vertical_alignment=ft.MainAxisAlignment.START,
        #             horizontal_alignment=ft.CrossAxisAlignment.CENTER
        #         )
        #     )

        # Приветственная страница

        if page.route == "/home":

            page.views.append(
                ft.View(
                    route="/home",
                    controls=[
                        ft.Text("Updating data...", font_family="LemonMilkBold", size=30),
                        ft.ProgressBar(),
                    ],
                    spacing=50,
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )

            page.update()

            await ensure_data()

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
                    share.get("volume"),
                    share.get("ticker"),
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
                    share.get("volume"),
                    share.get("ticker"),
                    share.get("new"),
                    page
                )
                shares_list.controls.append(scc.create_card())

            page.views.clear()

            # Add the sorted share cards to the view
            page.views.append(
                ft.View(
                    route='/home',
                    controls=[
                        ft.Text("Bot Broker", font_family="LemonMilkBold", size=50),
                        ft.Text("AI-POWERED", font_family="LemonMilkBold", size=15),
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

        elif str(page.route).startswith("/about:"):

            ticker = str(page.route).split(":")[-1]

            data = get_json("shares_list")

            shares_data = data.load_json().get("shares", [])
            share_data = next((share for share in shares_data if share["ticker"] == ticker), None)

            def change_text(change_day):
                try:
                    if (change_day < 0):
                        return ft.Text(str(change_day) + "%", color=ft.colors.RED)
                    elif (change_day == 0):
                        return ft.Text("+" + str(change_day) + "%", color=ft.colors.ORANGE)
                    else:
                        return ft.Text("+" + str(change_day) + "%", color=ft.colors.GREEN)
                except:
                    return ft.Text("+/- N/A")


            # share_info = ft.Row(
            #     controls=[
            #         ft.Image(share_data.get("image")),
            #         ft.Column(
            #             controls=[
            #                 ft.Text("Name:" + share_data.get("name")),
            #                 ft.Text("Ticker:" + share_data.get("ticker")),
            #                 ft.Text("Current price:" + str(share_data.get("price_dollars")) + "$"),
            #                 change_text(share_data.get("change_day"))
            #             ]
            #         )
            #     ]
            # )

            share_info = ft.Column(
                controls=[],
                expand=True,
                scroll=ft.ScrollMode.AUTO
            )

            ai_analyse_text = ft.Text("AI analyse", size=35, font_family="LemonMilkBold")

            def ai_analyse(event):
                ai_analyse_text.value = "Analyse would appear here..."
                page.update()
                ai_analyse_text.value = predict_stock_trend(ticker)
                page.update()

            share_graph = get_share_graph(ticker, 10)
            ai_button = ft.IconButton(icon=ft.icons.AUTO_GRAPH, on_click=ai_analyse, icon_size=35, tooltip="AI analyse")

            back_button = ft.ElevatedButton("Back to home page", on_click=lambda _: page.go("/home"))

            scc = share_card_creator(
                share_data.get("name"),
                share_data.get("image"),
                share_data.get("price_dollars"),
                share_data.get("change_day"),
                share_data.get("prediction"),
                share_data.get("confidence"),
                share_data.get("volume"),
                share_data.get("ticker"),
                share_data.get("new"),
                page
            )
            share_info.controls.append(scc.create_card())

            page.views.append(
                ft.View(
                    route="/about:",
                    controls=[
                        share_info,
                        ft.Row(
                            controls=[
                                ft.Column(
                                    controls=[
                                        share_graph,
                                        ft.Row(
                                            controls=[
                                                ai_analyse_text,
                                                ai_button
                                            ],
                                        ),

                                        back_button,
                                    ],
                                )
                            ],
                        )
                    ],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                    scroll=ft.ScrollMode.AUTO
                )
            )

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


async def ensure_data():
    data = get_json("shares_list")
    loaded_data = data.load_json()

    # Iterate through each share in the loaded data
    for share in loaded_data.get("shares", []):
        try:
<<<<<<< HEAD
            ticker = share.get("ticker")
            parsed_data = get_share_info(ticker)  # Ensure get_share_info is async
            print(parsed_data)

            # Check for valid parsed data
            if parsed_data.get("price") is None or parsed_data.get("percentage_change") is None:
                raise ValueError(f"No valid data for ticker {ticker}")

            # Apply rounding directly before saving to the dictionary
            share["price_dollars"] = round(float(parsed_data.get("price")), 4)
            share["change_day"] = round(float(parsed_data.get("percentage_change")), 4)
            share["volume"] = int(parsed_data.get("volume"))

        except Exception as e:
            print(f"Error processing share data for {share.get('name')}: {str(e)}")

            # Fall back to last known good data from JSON if available
            last_valid_price = share.get("price_dollars", None)
            last_valid_change_day = share.get("change_day", None)
            last_valid_volume = share.get("volume", None)

            if last_valid_price is not None and last_valid_change_day is not None:
                share["price_dollars"] = last_valid_price
                share["change_day"] = last_valid_change_day
                share["volume"] = last_valid_volume if last_valid_volume is not None else "N/A"

                # Calculate prediction and confidence based on last known data
                change_day = last_valid_change_day

                def clamp_confidence(confidence):
                    return round(max(0.05, min(confidence, 9.93)), 4)

                if change_day > 0 and change_day <= 1:
                    share["prediction"] = "Sell"
                    confidence = round(change_day, 4) - round(random.uniform(0.01, 0.1), 4)
                    share["confidence"] = clamp_confidence(confidence)
                elif change_day > 1:
                    share["prediction"] = "Sell"
                    confidence = 1 - round(random.uniform(0.01, 0.1), 4)
                    share["confidence"] = clamp_confidence(confidence)
                elif change_day < 0 and change_day >= -1:
                    share["prediction"] = "Buy"
                    confidence = round(abs(change_day), 4) - round(random.uniform(0.01, 0.1), 4)
                    share["confidence"] = clamp_confidence(confidence)
                elif change_day < -1:
                    share["prediction"] = "Buy"
                    confidence = 1 - round(random.uniform(0.01, 0.1), 4)
                    share["confidence"] = clamp_confidence(confidence)
                else:
                    share["prediction"] = "Keep"
                    share["confidence"] = round(1, 4)
            else:
                share["prediction"] = "N/A"
                share["confidence"] = "N/A"
                share["volume"] = "N/A"

    # Save the updated data back to the JSON file with rounded values
    with open("assets/shares_list.json", "w") as file:
        json.dump(loaded_data, file, indent=4)
=======
            ticker = share.get("ticker")  # Adjust based on your actual JSON structure
            parsed_data = await get_share_info(ticker)  # Make sure get_share_info is async if necessary
            print(parsed_data)

            # Update the dictionary with the new data
            share["price_dollars"] = parsed_data.get("price")
            share["change_day"] = parsed_data.get("percentage_change")

            def clamp_confidence(confidence):
                # Ensure the confidence is between 0.05 and 9.9
                return max(0.05, min(confidence, 9.93))

            if share.get("change_day") > 0 and share.get("change_day") <= 1:
                share["prediction"] = "Sell"
                confidence = round(share.get("change_day"), 4) - round(random.uniform(0.01, 0.1), 4)
                share["confidence"] = clamp_confidence(confidence)

            elif share.get("change_day") > 1:
                share["prediction"] = "Sell"
                confidence = 1 - round(random.uniform(0.01, 0.1), 4)
                share["confidence"] = clamp_confidence(confidence)

            elif share.get("change_day") < 0 and share.get("change_day") >= -1:
                share["prediction"] = "Buy"
                confidence = round(share.get("change_day") * -1, 4) - round(random.uniform(0.01, 0.1), 4)
                share["confidence"] = clamp_confidence(confidence)

            elif share.get("change_day") < -1:
                share["prediction"] = "Buy"
                confidence = 1 - round(random.uniform(0.01, 0.1), 4)
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
>>>>>>> 27c601ff6a7dc7d643b47abbc13c7cf92fdbdbb4

# Run Flet app in the main thread
if __name__ == "__main__":
    # Run Flet app in the main thread
    ft.app(target=main, assets_dir='assets', view=ft.AppView.WEB_BROWSER)