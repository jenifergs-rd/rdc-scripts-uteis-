const db_tallos_megasac = db.getSiblingDB('tallos-megasac');
const companyId = ObjectId('652e778c5f8b2357ffdefc01');

const currentDate = new Date();
const closeCallsAfter = 24; //tempo em horas

const findCustomersQuery = {
  company: companyId,
  on_call: true,
  reallocated_on_call: { '$in': [ false, null ] },
  last_interaction: { $lt: new Date(Date.now() - closeCallsAfter * 3600000) },
}

const customers = db_tallos_megasac.customers.find(findCustomersQuery)

const customersLength = customers.count()

print('Total de customers: '+customersLength+'\n')




// TESTE LISTAR FILA DE ESPERA EM RUBY
company_id = '63fce1e7788fd08e7c2709f2'
current_date = new Date()
close_calls_after = 99

query = {
  'company': company_id,
  'on_call': true,
  'reallocated_on_call': false,
  'last_interaction': current_date - (close_calls_after * 3600)
}       


customers = db.customers.find(query)

customers_length = customers.count