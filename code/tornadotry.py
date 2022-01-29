# import tornado.autoreload
# import tornado.ioloop
# import tornado.web
# import tornado.websocket
# import tornado.escape
# import tornado.gen
#
# class MainHandler(tornado.web.RequestHandler):
#     def get(self):
#         self.write('<a href="%s">link to story 1</a>' %
#                    self.reverse_url("thestory", "1"))
#
# class StoryHandler(tornado.web.RequestHandler):
#     def initialize(self, db):
#         self.db = db
#
#     def get(self, story_id):
#         self.write("this is story %s" % story_id)
#
#
# db = 2
# app = tornado.web.Application([
#     tornado.web.url(r"/", MainHandler),
#     tornado.web.url(r"/story/([0-9]+)", StoryHandler, dict(db=db), name="thestory")
#     ])
#
#
# app.listen(8889)
# tornado.ioloop.IOLoop.current().start()