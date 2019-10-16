##Models 

Models push some business logic throughout whole application.

<b>Base</b> model doesnt have DB table (abstract model). It has more extended version BaseOwned model. 
Base model should be inherited for objects responsibility for which isn't supposed to be fixed on some employee.
If you whould like to see responsible person for specific object (like an Order or a Deal) you should inherit object's model from BaseOwned.

<b>Client</b> model suits the need to common place for all types of clients. It is needed to find common logic - like telephones, names of clients to be put in 1 db table and be found easily. However some additional thought process needed when you want to exclude some client type from a client's view. Because we want to see person responsible for communication with client we inherit Client model from BaseOwned 
All client's types should be inherited from Client.

<b>Activity</b> model is a parent model for all acitvities types. All activities in CRM should be planned and tracked. So activity should have an owner (child of BaseOwned) and planned/fact dates.