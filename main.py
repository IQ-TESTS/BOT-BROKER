import flet as ft
import json

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


def main(page: Page):
    with open("shares_list.json", "r") as file:
        data = json.load(file)

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

            page.views.clear()

            # Add the sorted share cards to the view
            page.add(
                ft.Container(
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


flet.app(target=main, assets_dir="assets")
