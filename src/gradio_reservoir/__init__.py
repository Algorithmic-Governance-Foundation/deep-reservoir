import gradio as gr


def greet(name, age):
    return f"Hello {name}! You are {age} years old."


COUNTRIES_PLACEHOLDER = "country\nNew Zealand\nVietnam\nAustralia"
POLICIES_PLACEHOLDER = (
    "policy\nBagels can be eaten for lunch\nChicken salt is allowed on fries"
)


def main():
    demo = gr.Interface(
        fn=greet,
        inputs=[
            gr.Textbox(
                label="countries.csv", lines=20, placeholder=COUNTRIES_PLACEHOLDER
            ),
            gr.TextArea(
                label="policies.csv", lines=20, placeholder=POLICIES_PLACEHOLDER
            ),
        ],
        outputs=gr.Textbox(label="output.csv", lines=40),
    )
    demo.launch()


if __name__ == "__main__":
    main()
