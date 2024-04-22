// encontra mensagens do chip
db.messages.find({company: ObjectId('651f1d8e3847b77baf67e73a'), "channel_metadata.phone": "5511948772884"}).count()

// deleta as mensagens do chip
db.messages.deleteMany({company: ObjectId('651f1d8e3847b77baf67e73a'), "channel_metadata.phone": "5511948772884"})