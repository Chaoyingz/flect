from pydantic import BaseModel


class Config(BaseModel):
    debug: bool = False

    def render_to_html(self) -> str:
        html = ""

        debug_string = "true" if self.debug else ""
        html += f'<meta name="flect:debug" content="{debug_string}">'
        return html
