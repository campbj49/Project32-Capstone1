from app import app
from unittest import TestCase


class LoggedOutViewsTestCases(TestCase):
    """Bank of tests that don't require user login"""
    #adapting example code from Flask Testing module to current project
    
    #Enable WTforms to be tested
    def setUp(self):
        app.config['WTF_CSRF_ENABLED'] = False


    def test_landing_page(self):
        """Ensure root URL redirects successfully"""
        with app.test_client() as client:
            resp = client.get('/', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Register User', html, "Not redirecting to register user page.")

            
    def test_registration_page(self):
        """Checks that the registration page loads correctly"""
        with app.test_client() as client:
            resp = client.get('/register')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Register User', html)

            
    def test_logged_out_pages(self):
        """Checks that all the user specific pages throw errors when not logged in"""
        with app.test_client() as client:
            userPaths = (["/user/campbj49",
                          "/users/campbj49/character/add",
                          "/character/1/update",
                          "/character/1/delete",
                          "/character/1/inventory",
                          "/character/1/inventory/add"])
            for path in userPaths:
                resp = client.get(path, follow_redirects=True)
                html = resp.get_data(as_text=True)

                self.assertEqual(resp.status_code, 200, f"{path} has an issue")
                self.assertIn('Restricted page access attempted. Login first', html, f"${path} does not throw an error when no user is logged in")

    def test_item_list(self):
        """Ensures the item list page is loading"""
        with app.test_client() as client:
            resp = client.get('/item')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Item List', html)
            

    def test_item_routes(self):
        """Ensures the add/update/delete item pages function"""
        with app.test_client() as client:
            resp = client.post(
                '/item/add', data={
                    "name" :"testName",
                    "desc" : "testDescription",
                    "weight" : 3,
                    "image_url":"testUrl"
                },
                follow_redirects=True
            )
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('testName', html, "Item creation not functioning")
            
            #get created item's id
            end = start = html.find("testUrl")+33
            while html[end] != "/": end+=1
            item_id = html[start:end]

            #test update path
            resp = client.post(
                f'/item/{item_id}/update', data={
                    "name" :"testUpdateName",
                    "desc" : "testUpdateDescription",
                    "weight" : 3,
                    "image_url":"testUpdateUrl"
                },
                follow_redirects=True
            )
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('testUpdateName', html, "Item updating not functioning")

            #test delete path to keep server clean of test items
            resp = client.get(
                f'/item/{item_id}/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('testUpdateName', html, "Item deletion not functioning")


    def test_login_page(self):
        """Make sure login in functions correctly"""
        with app.test_client() as client:
            resp = client.post(
                '/login', data={
                    'username':'test',
                    'password':'test'
                },
                follow_redirects=True
            )
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("test&#39;s Characters", html,"Login not working")


class LoggedInViewsTestCases(TestCase):
    """Bank of tests for logged in user"""

    def setUp(self):
        #enable forms to be tested
        app.config['WTF_CSRF_ENABLED'] = False
        

    def test_redirects(self):
        """Checks that all the unauthorized access routes redirect 
            back to the home screen with an error"""
        with app.test_client() as client:
            #log in
            client.post(
                '/login', data={
                    'username':'test',
                    'password':'test'})         
            userPaths = (["/user/campbj49",
                          "/users/campbj49/character/add",
                          "/character/1/update",
                          "/character/1/delete",
                          "/character/1/inventory",
                          "/character/1/inventory/add"])
            for path in userPaths:
                resp = client.get(path, follow_redirects=True)
                html = resp.get_data(as_text=True)

                self.assertEqual(resp.status_code, 200, f"{path} has an issue")
                self.assertIn('Restricted page access attempted. Login first', html, f"${path} does not throw an error when the wrong user is logged in")
                self.assertIn("test&#39;s Characters", html,f"${path} 's restricted redirect does not return to homepage.")


    def test_character_routes(self):
        """Checks character creation, modification, and deletion routes"""
        with app.test_client() as client:
            #log in
            client.post(
                '/login', data={
                    'username':'test',
                    'password':'test'})  
            #create character
            resp = client.post(
                '/users/test/character/add', data={
                    "name" :"testName",
                    "bio" : "testBio",
                    "str_score" : 3,
                    "image_url":"testUrl",
                    "username":"test"
                },
                follow_redirects=True
            )
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('testName', html, "Character creation not functioning")
            
            #get created character's id
            end = start = html.find("testBio")+40
            while html[end] != "/": end+=1
            character_id = html[start:end]

            #test update path
            resp = client.post(
                f'/character/{character_id}/update', data={
                    "name" :"testUpdateName",
                    "bio" : "testUpdateDescription",
                    "str_score" : 3,
                    "image_url":"testUpdateUrl"
                },
                follow_redirects=True
            )
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('testUpdateName', html, "Character updating not functioning")

            #test delete path and remove test character from the server
            resp = client.get(
                f'/character/{character_id}/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('testUpdateName', html, "Character deletion not functioning")

    def test_inventory_routes(self):
        """Check inventory item addition, modification, and deletion routes"""
        with app.test_client() as client:
            #log in
            client.post(
                '/login', data={
                    'username':'test',
                    'password':'test'})  
            #create inventory_item
            resp = client.post(
                '/character/10/inventory/add', data={
                    "added-item":4}
                follow_redirects=True
            )
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('testName', html, "Inventory item creation not functioning")
            
            #get created inventory_item's id
            end = start = html.find("/character/10/",html.find("/character/10/inventory/add"))+14
            while html[end] != "/": end+=1
            inventory_item_id = html[start:end]
            self.assertEqual(inventory_item_id, 500)

            #test update path
            resp = client.post(
                f'/inventory_item/{inventory_item_id}/update', data={
                    "name" :"testUpdateName",
                    "bio" : "testUpdateDescription",
                    "str_score" : 3,
                    "image_url":"testUpdateUrl"
                },
                follow_redirects=True
            )
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('testUpdateName', html, "Inventory item updating not functioning")

            #test delete path and remove test inventory_item from the server
            resp = client.get(
                f'/inventory_item/{inventory_item_id}/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('testUpdateName', html, "Inventory item deletion not functioning")
