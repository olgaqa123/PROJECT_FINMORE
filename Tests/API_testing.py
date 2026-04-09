import time
import base64
import unittest
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
 
# =====================================================================
# Конфігурація
# =====================================================================
BASE_URL = "https://dev.emeli.in.ua/wp-json/wp/v2"
POSTS_ENDPOINT = f"{BASE_URL}/posts"
 
AUTH = {
    "username": "admin",
    "password": "Engineer_123",
}
 
 
def get_auth_headers() -> dict:
    """Повертає базові заголовки з Basic-авторизацією."""
    credentials = f"{AUTH['username']}:{AUTH['password']}"
    encoded = base64.b64encode(credentials.encode()).decode()
    return {
        "Authorization": f"Basic {encoded}",
        "Content-Type": "application/json",
    }
 
 
# =====================================================================
# CRUD тести
# =====================================================================
class TestWordPressPostsCRUD(unittest.TestCase):
    """WordPress Posts API — CRUD Tests"""
 
    created_post_id: int | None = None
 
    # ------------------------------------------------------------------
    # CREATE
    # ------------------------------------------------------------------
    def test_01_create_should_create_new_post(self):
        """CREATE — Should create a new post"""
        post_data = {
            "date": "2026-04-09T15:42:34",
            "date_gmt": "2026-04-09T15:42:34",
            "title": "Test Post from Python Requests",
            "content": "This is test content created via API automation",
            "status": "publish",
            "excerpt": "Test excerpt",
            "slug": "abcd"
            
        }
 
        response = requests.post(
            POSTS_ENDPOINT, headers=get_auth_headers(), json=post_data
        )
 
        self.assertTrue(response.ok, f"Response not OK: {response.text}")
        self.assertEqual(response.status_code, 201)
 
        body = response.json()
        TestWordPressPostsCRUD.created_post_id = body["id"]
 
        self.assertIn("id", body)
        self.assertIn("date", body)
        self.assertIn("date_gmt", body)
        self.assertIn("slug", body)
        self.assertIn("status", body)
        self.assertIn("password", body)
        self.assertIn("title", body)
        self.assertIn("content", body)
        self.assertIn("author", body)
        self.assertIn("excerpt", body)
        self.assertIn("featured_media", body)
        self.assertIn("comment_status", body)
        self.assertIn("ping_status", body)
        self.assertIn("format", body)
        self.assertIn("meta", body)
        self.assertIn("sticky", body)
        self.assertIn("template", body)
        self.assertIn("categories", body)
        self.assertIn("tags", body)
        self.assertNotIn("force", body)
        self.assertIn("link", body)

        self.assertEqual(body["date"], post_data["date"])
        self.assertEqual(body["date_gmt"], post_data["date_gmt"])
        self.assertNotEqual(body["slug"], "123av")
        #self.assertEqual(body["slug"], "")
        self.assertEqual(body["slug"], "abcd")
        self.assertEqual(body["status"], "publish")
        self.assertEqual(body["password"], "")
        self.assertEqual(body["title"]["raw"], post_data["title"])
        self.assertEqual(body["title"]["rendered"], post_data["title"])
        self.assertEqual(body["content"]["raw"], post_data["content"])
        self.assertEqual(body["content"]["rendered"], '<p>This is test content created via API automation</p>\n')
        self.assertEqual(body["content"]["protected"], False)
        self.assertEqual(body["content"]["block_version"], 0)
        self.assertEqual(body["author"], 1)
        self.assertEqual(body["excerpt"]["raw"], post_data["excerpt"])
        self.assertEqual(body["featured_media"], 0)
        self.assertEqual(body["comment_status"], "open")
        self.assertEqual(body["ping_status"], "open")
        self.assertEqual(body["format"], "standard")
        self.assertEqual(body["meta"]["footnotes"], "")
        self.assertEqual(body["sticky"], False)
        self.assertEqual(body["template"], "")
        self.assertEqual(body["categories"], [1])
        self.assertEqual(body["tags"], [])
        self.assertNotEqual(body["link"], "")

        print(f"Created post ID: {TestWordPressPostsCRUD.created_post_id}")
 
    # ------------------------------------------------------------------
    # READ — all posts
    # ------------------------------------------------------------------
    def test_02_read_should_get_all_posts(self):
        """READ — Should get all posts"""
        response = requests.get(POSTS_ENDPOINT)
 
        self.assertTrue(response.ok)
        self.assertEqual(response.status_code, 200)
 
        posts = response.json()
        self.assertIsInstance(posts, list)
        self.assertGreater(len(posts), 0)
 
        first_post = posts[0]
        self.assertIn("id", first_post)
        self.assertIn("title", first_post)
        self.assertIn("content", first_post)
 
    # ------------------------------------------------------------------
    # READ — single post
    # ------------------------------------------------------------------
    def test_03_read_should_get_specific_post_by_id(self):
        """READ — Should get a specific post by ID"""
        test_post_id = TestWordPressPostsCRUD.created_post_id or 1
 
        response = requests.get(f"{POSTS_ENDPOINT}/{test_post_id}")
 
        self.assertTrue(response.ok)
        self.assertEqual(response.status_code, 200)
 
        post = response.json()
        self.assertEqual(post["id"], test_post_id)
        self.assertIn("title", post)
        self.assertIn("content", post)
        self.assertIn("date", post)
 
    # ------------------------------------------------------------------
    # UPDATE (PUT)
    # ------------------------------------------------------------------
    def test_04_update_should_update_existing_post(self):
        """UPDATE — Should update an existing post"""
        if not TestWordPressPostsCRUD.created_post_id:
            self.skipTest("No post created to update")
 
        update_data = {
            "title": "Updated Test Post",
            "content": "This content has been updated via API",
            "excerpt": "Updated excerpt",
        }
 
        response = requests.put(
            f"{POSTS_ENDPOINT}/{TestWordPressPostsCRUD.created_post_id}",
            headers=get_auth_headers(),
            json=update_data,
        )
 
        self.assertTrue(response.ok)
        self.assertEqual(response.status_code, 200)
 
        updated_post = response.json()
        self.assertEqual(updated_post["id"], TestWordPressPostsCRUD.created_post_id)
        self.assertEqual(updated_post["title"]["rendered"], update_data["title"])
        self.assertIn("updated", updated_post["content"]["rendered"])
 
    # ------------------------------------------------------------------
    # PATCH
    # ------------------------------------------------------------------
    def test_05_patch_should_partially_update_post(self):
        """PATCH — Should partially update a post"""
        if not TestWordPressPostsCRUD.created_post_id:
            self.skipTest("No post created to patch")
 
        patch_data = {"title": "Patched Title Only"}
 
        response = requests.patch(
            f"{POSTS_ENDPOINT}/{TestWordPressPostsCRUD.created_post_id}",
            headers=get_auth_headers(),
            json=patch_data,
        )
 
        self.assertTrue(response.ok)
 
        patched_post = response.json()
        self.assertEqual(patched_post["title"]["rendered"], patch_data["title"])
 
    # ------------------------------------------------------------------
    # DELETE
    # ------------------------------------------------------------------
    def test_06_delete_should_delete_post(self):
        """DELETE — Should delete a post"""
        if not TestWordPressPostsCRUD.created_post_id:
            self.skipTest("No post created to delete")
 
        response = requests.delete(
            f"{POSTS_ENDPOINT}/{TestWordPressPostsCRUD.created_post_id}",
            headers=get_auth_headers(),
        )
 
        self.assertTrue(response.ok)
        self.assertEqual(response.status_code, 200)
 
        deleted_post = response.json()
        self.assertTrue(deleted_post.get("deleted"))
 
        # Перевіряємо, що пост справді видалено
        get_response = requests.get(
            f"{POSTS_ENDPOINT}/{TestWordPressPostsCRUD.created_post_id}"
        )
        self.assertEqual(get_response.status_code, 404)
 
    # ------------------------------------------------------------------
    # Error handling — 404
    # ------------------------------------------------------------------
    def test_07_error_404_for_nonexistent_post(self):
        """Error Handling — Should return 404 for non-existent post"""
        response = requests.get(f"{POSTS_ENDPOINT}/999999")
 
        self.assertEqual(response.status_code, 404)
 
        error_body = response.json()
        self.assertIn("code", error_body)
 
    # ------------------------------------------------------------------
    # Error handling — 401
    # ------------------------------------------------------------------
    def test_08_error_401_for_unauthorized_create(self):
        """Error Handling — Should return 401 for unauthorized create"""
        post_data = {
            "title": "Unauthorized Post",
            "content": "This should fail",
            "status": "publish",
        }
 
        # Без заголовку авторизації
        response = requests.post(
            POSTS_ENDPOINT,
            headers={"Content-Type": "application/json"},
            json=post_data,
        )
 
        self.assertEqual(response.status_code, 401)
 
    # ------------------------------------------------------------------
    # Filtering
    # ------------------------------------------------------------------
    def test_09_filtering_by_status(self):
        """Filtering — Should filter posts by status"""
        response = requests.get(f"{POSTS_ENDPOINT}?status=publish")
 
        self.assertTrue(response.ok)
 
        posts = response.json()
        for post in posts:
            self.assertEqual(post["status"], "publish")
 
    # ------------------------------------------------------------------
    # Pagination
    # ------------------------------------------------------------------
    def test_10_pagination_per_page_param(self):
        """Pagination — Should respect per_page parameter"""
        per_page = 5
        response = requests.get(f"{POSTS_ENDPOINT}?per_page={per_page}")
 
        self.assertTrue(response.ok)
 
        posts = response.json()
        self.assertLessEqual(len(posts), per_page)
 
 
# =====================================================================
# Validation тести
# =====================================================================
class TestWordPressPostsValidation(unittest.TestCase):
    """WordPress Posts API — Validation Tests"""
 
    def test_validate_required_fields(self):
        """Should validate required fields"""
        invalid_data = {
            # Відсутній обов'язковий title
            "content": "Content without title"
        }
 
        response = requests.post(
            POSTS_ENDPOINT, headers=get_auth_headers(), json=invalid_data
        )
 
        body = response.json()
        print(f"Validation response: {body}")
 
    def test_special_characters_in_title(self):
        """Should handle special characters in title"""
        special_data = {
            "title": 'Test with 特殊字符 & symbols <>"',
            "content": "Testing special characters",
            "status": "draft",
        }
 
        response = requests.post(
            POSTS_ENDPOINT, headers=get_auth_headers(), json=special_data
        )
 
        self.assertTrue(response.ok)
 
        post = response.json()
        self.assertIn("特殊字符", post["title"]["rendered"])
 
        # Cleanup
        requests.delete(
            f"{POSTS_ENDPOINT}/{post['id']}", headers=get_auth_headers()
        )
 
 
# =====================================================================
# Performance тести
# =====================================================================
class TestWordPressPostsPerformance(unittest.TestCase):
    """WordPress Posts API — Performance Tests"""
 
    def test_get_all_posts_response_time(self):
        """GET all posts — should respond within acceptable time"""
        start = time.time()
        response = requests.get(POSTS_ENDPOINT)
        elapsed_ms = (time.time() - start) * 1000
 
        self.assertTrue(response.ok)
        print(f"GET all posts response time: {elapsed_ms:.0f}ms")
 
        self.assertLess(elapsed_ms, 2000)
 
        if elapsed_ms > 1000:
            print(f"⚠️  Warning: Response time {elapsed_ms:.0f}ms exceeds 1 second")
 
    def test_get_single_post_response_time(self):
        """GET single post — should respond within acceptable time"""
        start = time.time()
        response = requests.get(f"{POSTS_ENDPOINT}/1")
        elapsed_ms = (time.time() - start) * 1000
 
        print(f"GET single post response time: {elapsed_ms:.0f}ms")
        self.assertLess(elapsed_ms, 1500)
 
        if elapsed_ms > 800:
            print(f"⚠️  Warning: Single post response time {elapsed_ms:.0f}ms exceeds 800ms")
 
    def test_post_create_response_time(self):
        """POST create post — should respond within acceptable time"""
        post_data = {
            "title": "Performance Test Post",
            "content": "Testing POST request speed",
            "status": "draft",
        }
 
        start = time.time()
        response = requests.post(
            POSTS_ENDPOINT, headers=get_auth_headers(), json=post_data
        )
        elapsed_ms = (time.time() - start) * 1000
 
        self.assertTrue(response.ok)
        print(f"POST create post response time: {elapsed_ms:.0f}ms")
        self.assertLess(elapsed_ms, 3000)
 
        # Cleanup
        post = response.json()
        requests.delete(f"{POSTS_ENDPOINT}/{post['id']}", headers=get_auth_headers())
 
    def test_put_update_response_time(self):
        """PUT update post — should respond within acceptable time"""
        # Створюємо пост
        create_resp = requests.post(
            POSTS_ENDPOINT,
            headers=get_auth_headers(),
            json={"title": "Post to Update", "content": "Initial content", "status": "draft"},
        )
        post_id = create_resp.json()["id"]
 
        update_data = {"title": "Updated Title", "content": "Updated content"}
 
        start = time.time()
        response = requests.put(
            f"{POSTS_ENDPOINT}/{post_id}",
            headers=get_auth_headers(),
            json=update_data,
        )
        elapsed_ms = (time.time() - start) * 1000
 
        self.assertTrue(response.ok)
        print(f"PUT update post response time: {elapsed_ms:.0f}ms")
        self.assertLess(elapsed_ms, 3000)
 
        # Cleanup
        requests.delete(f"{POSTS_ENDPOINT}/{post_id}", headers=get_auth_headers())
 
    def test_delete_response_time(self):
        """DELETE post — should respond within acceptable time"""
        create_resp = requests.post(
            POSTS_ENDPOINT,
            headers=get_auth_headers(),
            json={"title": "Post to Delete", "content": "Will be deleted", "status": "draft"},
        )
        post_id = create_resp.json()["id"]
 
        start = time.time()
        response = requests.delete(
            f"{POSTS_ENDPOINT}/{post_id}", headers=get_auth_headers()
        )
        elapsed_ms = (time.time() - start) * 1000
 
        self.assertTrue(response.ok)
        print(f"DELETE post response time: {elapsed_ms:.0f}ms")
        self.assertLess(elapsed_ms, 2000)
 
    def test_concurrent_get_requests(self):
        """Multiple concurrent GET requests — average response time"""
        num_requests = 5
        response_times: list[float] = []
 
        def make_request(_):
            start = time.time()
            resp = requests.get(POSTS_ENDPOINT)
            elapsed = (time.time() - start) * 1000
            return resp, elapsed
 
        with ThreadPoolExecutor(max_workers=num_requests) as executor:
            futures = [executor.submit(make_request, i) for i in range(num_requests)]
            results = [f.result() for f in as_completed(futures)]
 
        for resp, elapsed in results:
            self.assertTrue(resp.ok)
            response_times.append(elapsed)
 
        avg = sum(response_times) / len(response_times)
        print(
            f"Concurrent requests stats:\n"
            f"  - Average: {avg:.2f}ms\n"
            f"  - Min: {min(response_times):.0f}ms\n"
            f"  - Max: {max(response_times):.0f}ms\n"
            f"  - All times: {', '.join(f'{t:.0f}' for t in response_times)}ms"
        )
 
        self.assertLess(avg, 2500)
 
    def test_sequential_load_requests(self):
        """Load test — Sequential requests performance"""
        num_requests = 10
        response_times: list[float] = []
        total_start = time.time()
 
        for _ in range(num_requests):
            start = time.time()
            response = requests.get(f"{POSTS_ENDPOINT}?per_page=5")
            elapsed = (time.time() - start) * 1000
            response_times.append(elapsed)
            self.assertTrue(response.ok)
 
        total_ms = (time.time() - total_start) * 1000
        avg = sum(response_times) / len(response_times)
 
        print(
            f"Sequential load test ({num_requests} requests):\n"
            f"  - Total time: {total_ms:.0f}ms\n"
            f"  - Average per request: {avg:.2f}ms\n"
            f"  - Requests per second: {num_requests / (total_ms / 1000):.2f}"
        )
 
        self.assertLess(avg, 2000)
 
    def test_response_time_by_pagination_size(self):
        """Response time by pagination size"""
        page_sizes = [1, 5, 10, 20, 50]
        results: list[dict] = []
 
        for size in page_sizes:
            start = time.time()
            response = requests.get(f"{POSTS_ENDPOINT}?per_page={size}")
            elapsed = (time.time() - start) * 1000
 
            self.assertTrue(response.ok)
            results.append({"size": size, "time": elapsed})
 
        print("Response time by page size:")
        for r in results:
            print(f"  - {r['size']} posts: {r['time']:.0f}ms")
            self.assertLess(r["time"], 3000)
 
 
# =====================================================================
# Точка входу
# =====================================================================
if __name__ == "__main__":
    unittest.main(verbosity=2)