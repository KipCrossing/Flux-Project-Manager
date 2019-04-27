function myFunction() {
  var resorce_contact = {
    'Funding' : 'ben.rushton@voteflux.org',
    'Social Media' : 'ben.ballingall@voteflux.org',
    'Campaign Materials' : 'daithi.ogliasain@voteflux.org,joanne.cotterill@voteflux.org',
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
      var body = "Resources are requested for project : \n"
      + "Project Number: " + (j+1)
      + "\n"+ project_nickname
      + "\n" + subtitle + "\n\nBy: " + volunteer + "\n\nDescription: " + description
      + "\n\nObjective: " + objective
      + "\n\nResources Requested: " + resorces
      + "\n" + description_resources
      + "\nExpected Outcomes: " + outcomes
      + "\n\nGo to the flux discord to discuss this project: discord.io/FluxParty";
      var subject = "[AUTO] New Project: " +(j+1)+" "+ project_nickname
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
