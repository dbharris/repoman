from repository.tests import *

class TestImagesController(TestController):

    def test_index(self):
        response = self.app.get(url('repository_images'))
        # Test response...

    def test_index_as_xml(self):
        response = self.app.get(url('formatted_repository_images', format='xml'))

    def test_create(self):
        response = self.app.post(url('repository_images'))

    def test_new(self):
        response = self.app.get(url('repository_new_image'))

    def test_new_as_xml(self):
        response = self.app.get(url('formatted_repository_new_image', format='xml'))

    def test_update(self):
        response = self.app.put(url('repository_image', id=1))

    def test_update_browser_fakeout(self):
        response = self.app.post(url('repository_image', id=1), params=dict(_method='put'))

    def test_delete(self):
        response = self.app.delete(url('repository_image', id=1))

    def test_delete_browser_fakeout(self):
        response = self.app.post(url('repository_image', id=1), params=dict(_method='delete'))

    def test_show(self):
        response = self.app.get(url('repository_image', id=1))

    def test_show_as_xml(self):
        response = self.app.get(url('formatted_repository_image', id=1, format='xml'))

    def test_edit(self):
        response = self.app.get(url('repository_edit_image', id=1))

    def test_edit_as_xml(self):
        response = self.app.get(url('formatted_repository_edit_image', id=1, format='xml'))
