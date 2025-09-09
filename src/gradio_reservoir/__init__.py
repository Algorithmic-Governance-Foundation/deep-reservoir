import gradio as gr


def greet(agent1, agent2, name, age):
    return f"Hello {name}! You are {age} years old."


COUNTRIES_PLACEHOLDER = "country\nNew Zealand\nVietnam\nAustralia"
POLICIES_PLACEHOLDER = "policy\nBagels can be eaten for dinner\nChicken salt is allowed on fries\nKangaroos are not to be ridden"


def main():
    demo = gr.Interface(
        fn=greet,
        inputs=[
            gr.Dropdown(["GPT 4.1", "GPT 4o-mini", "Sonar Pro"], label="Search Agent"),
            gr.Dropdown(
                ["GPT 4.1", "GPT 4o-mini", "Sonar Pro"], label="Summariser Agent"
            ),
            gr.Textbox(
                label="countries.csv", lines=5, placeholder=COUNTRIES_PLACEHOLDER
            ),
            gr.TextArea(
                label="policies.csv", lines=5, placeholder=POLICIES_PLACEHOLDER
            ),
        ],
        outputs=gr.Textbox(label="output.csv", lines=40),
    )
    demo.launch()


if __name__ == "__main__":
    main()
