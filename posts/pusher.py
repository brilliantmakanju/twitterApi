import pusher

pusher_client = pusher.Pusher(
  app_id='1611266',
  key='21f13a253a7349a7f69f',
  secret='2e934f6c2bc85d1c4b1a',
  cluster='eu',
  ssl=True
)

# pusher_client.trigger('chat', 'message', {

# })