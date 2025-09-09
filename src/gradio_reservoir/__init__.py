import gradio as gr


def greet(name, age):
    return f"Hello {name}! You are {age} years old."


def main():
    demo = gr.Interface(
        fn=greet,
        inputs=[
            gr.Textbox(label="countries.csv", lines=20, placeholder="country"),
            gr.TextArea(label="policies.csv", lines=20, placeholder="policy"),
        ],
        outputs=gr.Textbox(label="output.csv", lines=40),
    )
    demo.launch()


if __name__ == "__main__":
    main()
