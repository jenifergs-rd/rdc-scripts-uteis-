const db_tallos_megasac = db.getSiblingDB('tallos-megasac') // get db

const companyId = ObjectId('602aab90f7ed606b03f0cdea') // Company: Dedo Brinquedo
const customerId = '' // if you want to filter by customer

const callsAggregate = db_tallos_megasac.getCollection('calls').aggregate([
  {
    $match: {
      company: companyId,
    }
  },
  {
    $sort: {
      created_at: 1
    }
  },
  {
    $group: {
      _id: {
        customer: "$customer",
        created_at: {
          $dateToString: {
            format: "%Y-%m-%dT%H:%M:%S",
            date: "$created_at"
          }
        }
      },
      calls: { $push: "$$ROOT" },
      count: { $sum: 1 }
    }
  },
  {
    $match: {
      count: { $gt: 1 }
    }
  }
]).toArray()

callsAggregate.forEach((group) => {
  group.calls.forEach((call, index) => {
    if (index > 0) {
      db_tallos_megasac.messages.updateMany({ call: ObjectId(call._id) }, { $set: { call: ObjectId(group.calls[0]._id) } })
      db_tallos_megasac.calls.deleteOne({ _id: ObjectId(call._id) })
    }
  })
})