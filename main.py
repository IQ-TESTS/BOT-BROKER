import flet as ft
import json


def main(page: ft.Page):
    def create_card(name, image, price_dollars, change_day, prediction, confidence, new):
        # Define default text based on the 'new' status
        if new:
            new_text = ft.Text("Recently listed in an IPO", color=ft.colors.GREEN)
        else:
            new_text = ft.Text("")

        # Check if confidence and price are integers
        confidence_text = (
            str(round(confidence * 100, 2)) + "%"
            if isinstance(confidence, (int, float))
            else "N/A"
        )

        price_text = (
            str(price_dollars) + "$"
            if isinstance(price_dollars, (int, float))
            else "N/A"
        )

        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.ListTile(
                            leading=ft.Image(src=image),
                            title=ft.Text(name),
                            subtitle=new_text
                        ),
                        ft.Row(
                            [
                                ft.Text("Prediction: " + prediction),
                                ft.Text("Confidence: " + confidence_text),
                                ft.Text("Price: " + price_text),
                                ft.Text(str(change_day) + "%", color=ft.colors.RED)
                            ],
                            alignment=ft.MainAxisAlignment.END,
                        ),
                    ]
                ),
                height=115,
                width=page.window.width + 200,
                padding=10,
            )
        )

    with open("assets/shares_list.json", "r") as file:
        data = json.load(file)

    shares_list = ft.Column(
        controls=[],
        expand=True,
        scroll=ft.ScrollMode.AUTO
    )

    shares_data = data.get("shares", [])

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
        scc = create_card(
            share.get("name"),
            share.get("image"),
            share.get("price_dollars"),
            share.get("change_day"),
            share.get("prediction"),
            share.get("confidence"),
            share.get("new"),
        )
        shares_list.controls.append(scc)

    # Optionally, you can display cards for no_data_shares separately if needed
    for share in no_data_shares:
        scc = create_card(
            share.get("name"),
            share.get("image"),
            share.get("price_dollars"),
            share.get("change_day"),
            share.get("prediction"),
            share.get("confidence"),
            share.get("new"),
        )
        shares_list.controls.append(scc)


    # Add the sorted share cards to the view
    page.add(
        ft.Column(
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
        )
    )

    page.update()


ft.app(target=main, assets_dir="assets")
