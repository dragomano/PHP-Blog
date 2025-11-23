def on_post_page(output, page, config):
    return output.replace(
        "https://fonts.googleapis.com/css",
        "https://fonts.bunny.net/css"
    )
