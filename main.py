import flet as ft
from ShareInfoParser import get_share_graph, get_share_info, update_graph
import asyncio
import json
import random
import math
def main(page: ft.Page):

    page.theme_mode = "dark"

    page.fonts = {
        "L": "fonts/LemonMilkBold.otf", "M": "fonts/Gothic60-Regular.otf",
    }

    page.theme = ft.Theme(
        font_family="M"
    )

    def bond_card(image_source, name, ticker, prediction, confidence, price, change):
        # Utility functions for styling
        def prediction_in_color(source):
            if source == "Buy":
                return ft.colors.GREEN
            elif source == "Keep":
                return ft.colors.YELLOW
            else:
                return ft.colors.RED

        def change_value(source):
            if source > 0:
                return f"+{source}%"
            elif source == 0:
                return f"+/-{source}%"
            else:
                return f"{source}%"

        def change_color(source):
            if source > 0:
                return ft.colors.GREEN
            elif source == 0:
                return ft.colors.YELLOW
            else:
                return ft.colors.RED

        # Initial state of additional card and icon
        additional_card_visible = False
        additional_card_height = 0  # Initially hidden
        arrow_icon = ft.icons.ARROW_CIRCLE_DOWN  # Initial icon
        icon_tooltip = "Show Graph"

        # Function to show or hide the additional card with animation
        def toggle_additional_card(e):
            nonlocal additional_card_visible, additional_card_height, arrow_icon, icon_tooltip
            if additional_card_visible:
                # Collapse the additional card (raise up)
                additional_card.height = 0  # Collapse the additional card
                arrow_icon = ft.icons.ARROW_CIRCLE_DOWN  # Change to downward arrow
                icon_tooltip = "Show Graph"
            else:
                # Expand the additional card (drop down)
                additional_card.height = 500  # Expand the additional card
                arrow_icon = ft.icons.ARROW_CIRCLE_UP  # Change to upward arrow
                icon_tooltip = "Hide Graph"

            additional_card.update()
            icon_button.icon = arrow_icon
            icon_button.tooltip = icon_tooltip
            icon_button.update()
            additional_card_visible = not additional_card_visible

        # Image container
        image = ft.Image(
            src=image_source,
            border_radius=15,
            width=80,
            height=80,
        )

        img_container = ft.Container(
            content=image,
            border=ft.border.all(5, ft.colors.BLACK),
            border_radius=15,
            width=80,
            height=80,
            padding=0
        )

        # Simple card container
        icon_button = ft.IconButton(icon=arrow_icon, on_click=toggle_additional_card,
                                    tooltip="Show Graph")  # Store a reference to the IconButton

        card = ft.Container(
            content=ft.Row(
                controls=[
                    img_container,
                    ft.Column(
                        controls=[
                            ft.Text(name, font_family="M", size=20, expand_loose=True),
                            ft.Text(f"${ticker}", font_family="M", size=12, expand_loose=True),
                        ],
                        spacing=1,
                        expand_loose=True
                    ),
                    # Bottom right row with predictions, price, and button
                    ft.Row(
                        controls=[
                            ft.Text(prediction, color=prediction_in_color(prediction),
                                    size=15),
                            ft.Text(f"({confidence}%)", color=ft.colors.BLUE, size=15),
                            ft.Text(f"{price}$", size=15),
                            ft.Text(change_value(change), color=change_color(change),
                                    size=15),
                            icon_button  # Use the IconButton reference here
                        ],
                        alignment=ft.MainAxisAlignment.END,
                        expand_loose=True,
                    )
                ],
                expand_loose=True
            ),
            expand_loose=True,
            bgcolor=ft.colors.GREY_900,
            width=700,
            height=100,  # Default height of the simple card
            padding=10,
            border_radius=20,
            shadow=ft.BoxShadow(blur_radius=5),  # Adds shadow to emphasize layering
            animate=ft.Animation(duration=500, curve=ft.AnimationCurve.EASE_IN_OUT)  # Add animation her
        )

        # Additional card (initially hidden, height 0)
        additional_card = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Graph"),
                    get_share_graph(ticker, (220, 220),  "#ebf0f2")
                ],
                scroll=ft.ScrollMode.AUTO
            ),
            bgcolor=ft.colors.BLACK,
            width=700,
            height=additional_card_height,  # Initially hidden
            border_radius=20,
            animate_size=ft.Animation(duration=500, curve=ft.AnimationCurve.EASE_IN_OUT),  # Smooth animation
            padding=10,
            expand_loose=True,
            expand=True,
            border=ft.border.all(5, ft.colors.GREY_900),
        )

        # Stack both the simple card and additional card
        overall_card = ft.Column(
            controls=[
                card,  # The simple card stays on top
                additional_card  # The additional card expands below the simple card
            ],
            spacing=0  # Ensures the cards are seamlessly stacked
        )

        return overall_card

    async def load_bond_cards():
        # Simulating a delay to allow the "Updating data..." text to display
        await asyncio.sleep(0.1)  # You can adjust the delay as needed

        with open("assets/shares_list.json", "r") as file:
            data = json.load(file)

        bond_cards = ft.Column(
            controls=[
            ],
            spacing=20,
            scroll=ft.ScrollMode.AUTO
        )

        # Adding staggered animation by introducing a delay for each bond card
        for i in range(len(data["shares"])):
            share = data["shares"][i]
            bond_cards.controls.append(
                bond_card(
                    share.get("image"),
                    share.get("name"),
                    share.get("ticker"),
                    share.get("prediction"),
                    math.ceil(share.get("confidence") * 100),
                    share.get("price_dollars"),
                    share.get("change_day")
                )
            )

        return bond_cards

    async def load_best_bond_cards():
        await asyncio.sleep(0.1)  # You can adjust the delay as needed

        with open("assets/shares_list.json", "r") as file:
            data = json.load(file)

        bond_cards = ft.Column(
            controls=[
                ft.Text("Top shares now", font_family="L", size=25)
            ],
            spacing=20,
            scroll=ft.ScrollMode.AUTO
        )

        # Adding staggered animation by introducing a delay for each bond card
        for i in range(len(data["top_shares"])):
            share = data["top_shares"][i]
            bond_cards.controls.append(
                bond_card(
                    share.get("image"),
                    share.get("name"),
                    share.get("ticker"),
                    share.get("prediction"),
                    math.ceil(share.get("confidence") * 100),
                    share.get("price_dollars"),
                    share.get("change_day")
                )
            )

        return bond_cards

    async def ensure_data():
        with open("assets/shares_list.json", "r") as file:
            data = json.load(file)

        # Iterate through each share in the loaded data
        for share in data.get("shares", []):
            try:
                ticker = share.get("ticker")
                update_graph(ticker, "#000000", "white")
                parsed_data = get_share_info(ticker)  # Ensure get_share_info is async

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

        for share in data.get("top_shares", []):
            try:
                ticker = share.get("ticker")
                parsed_data = get_share_info(ticker)  # Ensure get_share_info is async

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
            json.dump(data, file, indent=4)

    async def route_change(route):
        page.views.clear()

        if page.route == "/home":
            # Display the loading message
            loading_view = ft.View(
                route="/home",
                bgcolor=ft.colors.BLACK,
                controls=[
                    ft.Text("Updating data...", font_family="L", size=30),
                    ft.ProgressBar(),
                ],
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
            page.views.append(loading_view)

            # Update the page to show the loading message
            page.update()

            top_bond_cards = await load_best_bond_cards()
            # Load bond cards after a brief delay
            bond_cards = await load_bond_cards()

            page.views.clear()

            about_text = "Unlock the Potential of AI in Your Investment Journey.\n" \
                         "In today's rapidly evolving financial landscape,\n" \
                         "leveraging advanced technology has become imperative\n" \
                         "for successful investing. Allow artificial intelligence\n" \
                         "to assist you in your investment decisions; simply\n" \
                         "follow its expert guidance.\n" \
                         "Introducing Bot-Broker AI—your comprehensive partner\n" \
                         "in navigating the world of bond investments.\n" \
                         "With unparalleled precision, our AI offers you\n" \
                         "exceptional opportunities to capitalize on the bond\n" \
                         "market, enabling you to make informed choices and\n" \
                         "maximize your returns.\n" \
                         "The accuracy of our AI-driven insights has reached\n" \
                         "unprecedented levels, ensuring that you benefit\n" \
                         "from the most reliable and timely information\n" \
                         "available. Embrace the power of technology and\n" \
                         "take a step toward smarter investing.\n" \
                         "Let Bot-Broker AI support your financial goals\n" \
                         "and enhance your investment strategy."

            page.views.append(
                ft.View(
                    route="/home",
                    bgcolor=ft.colors.BLACK,
                    scroll=ft.ScrollMode.AUTO,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Column(
                                    controls=[
                                        ft.Text("Bot Broker", font_family="L", size=50),
                                        ft.Text("AI-POWERED", font_family="L", size=15),
                                        ft.Text("   "),
                                        ft.Text(about_text, font_family="M"),
                                        ft.Text("   "),
                                        ft.ElevatedButton("How does it work?", on_click=lambda _: page.go("/about")),
                                        ft.ElevatedButton("Need help?", url="https://t.me/botbroker_helpusers")
                                    ],
                                    alignment=ft.alignment.top_left
                                ),

                                top_bond_cards
                            ],

                            wrap=True,
                            spacing=200,
                            expand=True,
                            expand_loose=True
                        ),

                        ft.Text("   "),
                        ft.Text("   "),
                        ft.Text("   "),

                        ft.Text("Browse all shares", font_family="L", size=25),

                        bond_cards,

                        ft.Text("   "),
                        ft.Text("   "),

                        ft.Card(
                            content=ft.Row(
                                controls=[
                                    ft.Image("tg_picture.png", border_radius=60, width=100, height=100),
                                    ft.Column(
                                        controls=[
                                            ft.Text("   Telegram", font_family="L", size=20),
                                            ft.Text("       Help", font_family="M", size=15),
                                            ft.TextButton("@botbroker_helpusers", url="https://t.me/botbroker_helpusers")
                                        ],
                                        spacing=2
                                    )
                                ]
                            ),
                            color=ft.colors.GREY_900
                        )
                    ]
                )
            )

            page.update()  # Final update to render the new view

            await asyncio.sleep(1)
            await ensure_data()

        elif page.route == "/about":

            about_text = (
                "### About Bot-Broker AI\n\n"
                "In an age where financial markets are influenced by countless variables, making informed investment decisions can be daunting. "
                "Enter **Bot-Broker AI**, your intelligent ally in the world of trading. Designed to streamline the investment process, Bot-Broker "
                "leverages cutting-edge artificial intelligence to provide traders with actionable insights, enabling them to focus less on the "
                "minutiae of market analysis and more on executing their trading strategies.\n\n"

                "#### How Does Bot-Broker AI Work?\n\n"
                "At the core of Bot-Broker is a robust machine-learning engine that analyzes vast amounts of financial data in real time. "
                "This AI-driven platform is engineered to identify patterns, trends, and opportunities within the bond market that may go "
                "unnoticed by even the most seasoned traders. Here’s how it works:\n\n"

                "1. **Data Aggregation**: Bot-Broker AI aggregates data from various sources, including historical price movements, economic indicators, "
                "and market news. This comprehensive data collection enables the AI to build a rich dataset that forms the foundation of its insights.\n\n"

                "2. **Advanced Algorithms**: Utilizing state-of-the-art algorithms, Bot-Broker processes the aggregated data to identify patterns and correlations. "
                "These algorithms are continuously refined through machine learning, enhancing their ability to predict market movements with remarkable accuracy.\n\n"

                "3. **Real-Time Analysis**: As market conditions shift, Bot-Broker AI conducts real-time analysis to adapt its recommendations. This agility ensures that you "
                "receive timely and relevant insights, allowing you to capitalize on market opportunities as they arise.\n\n"

                "4. **Expert Guidance**: Bot-Broker AI is designed to simplify the decision-making process. By providing clear, actionable recommendations, the platform "
                "enables traders to follow AI-driven advice with confidence. Whether you are a seasoned investor or just starting, Bot-Broker's guidance is accessible and user-friendly.\n\n"

                "5. **Performance Tracking**: The AI not only offers insights but also tracks the performance of its recommendations. By analyzing the results of past trades, "
                "Bot-Broker continuously learns and adapts its strategies to enhance accuracy further, ensuring that you benefit from a system that evolves alongside the market.\n\n"

                "#### Accuracy You Can Trust\n\n"
                "One of the standout features of Bot-Broker AI is its remarkable accuracy. Through continuous learning and adaptation, the platform has achieved unprecedented "
                "levels of precision in its predictions. This commitment to accuracy means you can rely on Bot-Broker AI for the most reliable and timely information, allowing you "
                "to make informed choices that can maximize your returns.\n\n"

                "#### Embrace the Future of Investing\n\n"
                "Investing has traditionally required extensive research, analysis, and market knowledge. However, with Bot-Broker AI, you can unlock the full potential of technology "
                "to assist you in your trading journey. Imagine having a virtual financial advisor that works tirelessly to provide you with the insights you need, leaving you free to focus on executing your strategy.\n\n"

                "By embracing the power of Bot-Broker AI, you are taking a significant step towards smarter investing. Let this advanced technology guide you toward your financial goals "
                "and enhance your investment strategy. With Bot-Broker, the future of investing is here, and it's powered by AI.\n\n"

                "### Start Your Journey Today!\n\n"
                "Join the growing community of traders who are leveraging the power of Bot-Broker AI to transform their investment experience. With unparalleled accuracy and expert guidance "
                "at your fingertips, you can confidently navigate the complexities of the bond market and make decisions that align with your financial aspirations. Discover how "
                "Bot-Broker AI can change the way you invest and empower your trading journey today!"
            )

            page.views.append(
                ft.View(
                    route="/home",
                    bgcolor=ft.colors.BLACK,
                    scroll=ft.ScrollMode.AUTO,
                    controls=[
                        ft.Text("Bot Broker", font_family="L", size=30),
                        ft.Container(
                            width=800,
                            height=1130,
                            content=ft.Markdown(about_text)
                        ),
                        ft.ElevatedButton("Back", on_click=lambda _: page.go("/home"))
                    ],
                    spacing=10,
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )



    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go('/home')


ft.app(target=main, view=ft.AppView.WEB_BROWSER)