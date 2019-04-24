function myFunction() {
  var resorce_contact = {
    'Funding' : 'ben.rushton@voteflux.org',
    'Social Media' : 'ben.ballingall@voteflux.org',
    'Campaign Materials' : 'joanne.cotterill@voteflux.org',
    'Permissions' : 'max.kaye@voteflux.org',
    'Other Volunteers' : 'joanne.cotterill@voteflux.org',
    'Nothing' : 'daithi.ogliasain@voteflux.org'
  };

  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var data = ss.getSheetByName("Form Responses 1").getDataRange().getValues();
  for (var j = 1; j < data.length; j++) {
    if(data[j][11] == ''){
      volunteer = data[j][1];
      subtitle = data[j][2];
      project_nickname = data[j][3];
      description = data[j][4];
      objective = data[j][6];
      resorces = data[j][6];
      resorces_list = resorces.split(", ");
      description_resources = data[j][7];
      outcomes = data[j][8];
      var body = "Resorces are requested for project : \n" + project_nickname
      + "\n" + subtitle + "\nBy: " + volunteer + "\nDescription: " + description
      + "\nObjective: " + objective
      + "\nResorces Requested: " + resorces
      + "\n" + description_resources
      + "\nExpected Outcomes: " + outcomes
      + "\n\n\n";
      var subject = "[AUTO] New Project: " + project_nickname
      Logger.log(subject);
      Logger.log(body);
      for(var i = 0; i < resorces_list.length; i++) {
        Logger.log("Send Email: " + resorce_contact[resorces_list[i]]);
        GmailApp.sendEmail(resorce_contact[resorces_list[i]],subject,body)


      }
      ss.getActiveSheet().getRange(j+1, 12).setValue("Sent")
    }

  }

}
