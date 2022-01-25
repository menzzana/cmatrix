<html>
  <head>
    <!--- The stylesheet is symbolically linked from the htdocs as cg-bin folder has execute only --->
    <link type="text/css" rel="stylesheet" href="/cmatrix/static/style.css" />
    <title>Competence Matrix</title>
  </head>
  <body>
    <div>
      <button class="unselbtn" onclick="window.location.href='cmatrix.py'">Competence matrix</button>
      <button class="unselbtn" onclick="window.location.href='competence.py'">Category competence</button>
      <button class="selbtn" onclick="window.location.href='pers_cmatrix.py'">Personal competence matrix</button>
      <button class="unselbtn" onclick="window.location.href='add_competence.py'">Add competence</button>
      User: {{username}}
    </div>
    <hr>
    <h1>Competence Matrix</h1>
    <form action="update.py?page=pers_cmatrix" method="post">
      <table>
      % cat=""
      % comp=""
      % for row in rows:
      %   if cat<>row['category']:
      %     cat=row['category']
            <tr><td><br><b>{{row['category']}}</b></td></tr>
      %     end
      %   if comp<>row['competence']:
      %     if len(comp)>0:
              </tr>
      %       end
            <tr><td>{{row['competence']}}</td>
      %     comp=row['competence']
      %     end
          <td>
          <select name={{row['id'] or row['competence']}} class="td_scale{{row['scale_id'] or 0}}" 
           onchange="this.className=this.options[this.selectedIndex].className" 
           class="td_scale"+this.options[this.selectedIndex]>
      %     for row2 in rowscale:
      %       sel_text=""
      %       if row['scale_id']==row2['id']:
      %         sel_text=" selected"
      %         end  
              <option value="{{row2['id']}}" class="td_scale{{row2['id']}}"{{sel_text}}>{{row2['name']}}</option>
      %       end
          </select></td>
      %   end
      </table>
      <br>
      <input  class="selbtn" value="Change competences" type="submit" />
    </form>
  </body>
</html>
