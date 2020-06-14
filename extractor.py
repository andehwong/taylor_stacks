class Extractor:

    @staticmethod
    def get_all_specified_data(html_raw, html_tag, class_name):
        return html_raw.find_all(html_tag, class_=class_name)
