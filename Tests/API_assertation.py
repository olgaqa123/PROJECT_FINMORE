#def assert_post_schema(testcase, body):
#    required_fields = [
#        "id",
#        "date",
#        "title",
#        "content",
#        "status",
#        "author",
#    ]
#    for field in required_fields:
#        testcase.assertIn(field, body)
 
 
#def assert_post_data(testcase, body, expected):
#    testcase.assertEqual(body["title"]["raw"], expected["title"])
#    testcase.assertEqual(body["content"]["raw"], expected["content"])
#    testcase.assertEqual(body["status"], expected["status"])

