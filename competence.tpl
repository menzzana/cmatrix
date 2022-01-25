<html>
  <head>
    <!--- The stylesheet is symbolically linked from the htdocs as cg-bin folder has execute only --->
    <link type="text/css" rel="stylesheet" href="/cmatrix/static/style.css" />
    <title>Competence Matrix</title>
  </head>
  <body>
    <div>
      <button class="unselbtn" onclick="window.location.href='cmatrix.py'">Competence matrix</button>
      <button class="selbtn" onclick="window.location.href='competence.py'">Category competence</button>
      <button class="unselbtn" onclick="window.location.href='pers_cmatrix.py'">Personal competence matrix</button>
      <button class="unselbtn" onclick="window.location.href='add_competence.py'">Add competence</button>
      User: {{username}}
    </div>
    <hr>
    <h2>Competence for
      <select onchange="window.location.href='competence.py?competence_id='+this.value">
      % for row in rowallcompetence:
      %   sel_text=""
      %   if row['name']==competence:
      %     sel_text=" selected"
      %     end
          <option value={{row['id']}}{{sel_text}}>{{row['name']}}</option>
      %   end
      </select></h2>
      <table>
      % for row in rowcompetence:
          <tr>
            <td>{{row['full_name']}}</td>
            <td class="td_scale{{row['scale_id']}}">{{rowscale[row['scale_id']]['name']}}</td>
          </tr>
      %   end
      </table>
  </body>
</html>
