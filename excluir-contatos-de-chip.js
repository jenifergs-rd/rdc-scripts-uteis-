// encontrar e contar numero de contatos

company = '65ce035e13e5bc5d162a710c'

db.customers.find({company: ObjectId(company), tags:tag}).count_documents

// deletar contatos encontrados
db.customers.deleteMany({company: ObjectId('651f1d8e3847b77baf67e73a'), "channel_metadata.integration": "integration-1"})

// buscar contatos pela tag/etiqueta dentro da company
// {company: ObjectId('64f08dc247901e2e0eac8952'), tags: {
//     $in: [
//         ObjectId('660bf969a1e713d7bca3c772'),
//         ObjectId('660bf969a1e713d7bca3c777'),
//         ObjectId('660bf969a1e713d7bca3c774')
//     ]
// }}



db.customers.find({company: ObjectId(company)}).count



// EM RUBY BUSCAR TODOS OS CONTATOS COM X TAG
tag = '65ea043ea1e713d7bc3f41fd'
db.customers.find({company: ObjectId(company), tags:ObjectId(tag)}).count()

// em ruby deletar contatos com a tag/etiqueta espeficicada
db.customers.deleteMany({company: ObjectId(company), tags:ObjectId(tag)})



// customers leandro:  910
// {company: ObjectId('65ce035e13e5bc5d162a710c'), tags: {
//     $in: [
//         ObjectId('65ea0476a1e713d7bc4214a6'),
//         ObjectId('65ea0476a1e713d7bc4214a7'),
//         ObjectId('65ea0476a1e713d7bc4214a8')
//     ]
// }}

// customers thiago 932
// {company: ObjectId('65ce035e13e5bc5d162a710c'), tags: {
//     $in: [
//         ObjectId('65ea04b0a1e713d7bc44bc5d'),
//         ObjectId('65ea04b0a1e713d7bc44bc5f'),
// 		ObjectId('65ea04b0a1e713d7bc44bc60')
//     ]
// }}

//customers shaiane 440
// {company: ObjectId('65ce035e13e5bc5d162a710c'), tags: {
//     $in: [
//         ObjectId('65ea04e6a1e713d7bc470e79'),
//         ObjectId('65ea04e6a1e713d7bc470e7e'),
// 		ObjectId('65ea04e6a1e713d7bc470e7c'),
// 		ObjectId('65ea04e6a1e713d7bc470e7b'),
// 		ObjectId('65ea04e6a1e713d7bc470e7f'),
        
//     ]
// }}

// customers madson 936
// {company: ObjectId('65ce035e13e5bc5d162a710c'), tags: {
//     $in: [
//         ObjectId('65ea043ea1e713d7bc3f41fc'),
//         ObjectId('65ea043ea1e713d7bc3f41fb'),
// 		ObjectId('65ea043ea1e713d7bc3f41fd')
//     ]
// }}
