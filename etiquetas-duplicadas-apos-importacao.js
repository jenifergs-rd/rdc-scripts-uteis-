/**
 *
 * Script que remove tags duplicadas da collection de tags
 * captura o id dessas tags e atualiza os customers que as possuam
 * removendo as tags com ids que foram removidos e atualizando para
 * o id das tags que permaneceram na base.
 *
 */
tallos_megasac = db.getSiblingDB('tallos-megasac');
company_id = ObjectId('6568d1a09a92b192f48d14b8');
tallos_megasac.tags.aggregate([
    { $match: { company: company_id } },
    { $group: {
        _id: {name: "$name", created_at: "$createdAt"},
        ids: {$push: "$_id"},
        count: {$sum: 1}
    } },
    { $match: { count: {$gt: 1} } }
]).forEach(tag => {
    saved_tags = tag.ids.shift();
    duplicated_tags = tag.ids;
    //print(duplicated_tags)
    tallos_megasac.tags.deleteMany({ company: company_id, _id: { $in: duplicated_tags } });
    tallos_megasac.customers.find({ company: company_id, tags: { $in: duplicated_tags } }, { _id: 1, full_name: 1, tags: 1 })
    .forEach(customer => {
        customer_condition = { _id: customer._id, company: company_id }
        tallos_megasac.customers.updateOne(
            customer_condition,
            { $pull: { tags: { $in: duplicated_tags } } }
        )
        print(saved_tags)
        tallos_megasac.customers.updateOne(
            customer_condition,
            { $push : { tags: { $each: [saved_tags] } }}
        )
        print(customer.full_name)
        print(customer.tags)
    })
});