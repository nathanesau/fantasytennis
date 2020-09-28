from unittest import TestCase
import app
import os.path


class TestApp(TestCase):

    RESOURCE_FOLDER = "{}/resources".format(
        os.path.dirname(os.path.realpath(__file__)))

    def test_download_archive(self):
        # 2019
        archive_filename = app.download_archive(2019)
        f = open(archive_filename, 'r')
        data = f.read()
        assert(data != None)

        # 2018
        archive_filename = app.download_archive(2018)
        f = open(archive_filename, 'r')
        data = f.read()
        assert(data != None)

    def test_parse_archive(self):
        # 2019
        archive_filename = "{}/archive/2019.html".format(TestApp.RESOURCE_FOLDER)
        archive_data = app.parse_archive(archive_filename)
        print(archive_data)

        # 2018
        archive_filename = "{}/archive/2018.html".format(TestApp.RESOURCE_FOLDER)
        archive_data = app.parse_archive(archive_filename)
        print(archive_data)

    def test_download_draw(self):
        # 2019 - ATP Masters 1000 Canada
        draw_info = {'title': 'ATP Masters 1000 Canada',
            'link': '/en/scores/archive/toronto/421/2018/draws?matchtype=singles',
            'year': 2019}
        draw_filename = app.download_draw(draw_info)
        f = open(draw_filename, 'r')
        data = f.read()
        assert(data != None)

        # 2018 - Shenzhen
        draw_info = {'title': 'Shenzhen',
            'link': '/en/scores/archive/shenzhen/6967/2018/draws?matchtype=singles',
            'year': 2018}
        draw_filename = app.download_draw(draw_info)
        f = open(draw_filename, 'r')
        data = f.read()
        assert(data != None)
    
    def test_parse_draw(self):
        # 2019 - ATP Masters 1000 Canada
        draw_filename = "{}/draw/2019/ATP_Masters_1000_Canada.html".format(
            TestApp.RESOURCE_FOLDER)
        draw_data = app.parse_draw(draw_filename)
        print(draw_data)

        # 2018 - Shenzhen
        draw_filename = "{}/draw/2018/Shenzhen.html".format(
            TestApp.RESOURCE_FOLDER)
        draw_data = app.parse_draw(draw_filename)
        print(draw_data)

    def test_write_draw_to_db(self):
        # 2019 - ATP Masters 1000 Canada
        draw_filename = "{}/draw/2019/ATP_Masters_1000_Canada.html".format(
            TestApp.RESOURCE_FOLDER)
        draw_data = app.parse_draw(draw_filename)
        app.write_draw_to_db(draw_data, {'title': 'ATP Masters 1000 Canada'})
