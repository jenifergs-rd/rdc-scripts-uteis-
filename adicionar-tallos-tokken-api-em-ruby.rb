

companyId = "65023acbe08e3c3478063a3d" 
db.companies.updateOne({ _id: ObjectId(companyId) }, 
{ $set: { "settings.tallos_tai_access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJyYXphb19zb2NpYWwiOiJVcGFyZ2FtZXMgTHRkYSIsImNucGoiOiIzODI5MDYyNjAwMDE1MiJ9.Y6h37wj5-yJ9E1S8SIraYls64_3MCf-oAfmBgkob8Y0" } })
