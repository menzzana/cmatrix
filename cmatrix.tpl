<html>
  <head>
    <!--- The stylesheet is symbolically linked from the htdocs as cg-bin folder has execute only --->
    <link type="text/css" rel="stylesheet" href="/cmatrix/static/style.css" />
    <title>Competence Matrix</title>
  </head>
  <body>
    <div>
      <button class="selbtn" onclick="window.location.href='cmatrix.py'">Competence matrix</button>
      <button class="unselbtn" onclick="window.location.href='competence.py'">Category competence</button>
      <button class="unselbtn" onclick="window.location.href='pers_cmatrix.py'">Personal competence matrix</button>
      <button class="unselbtn" onclick="window.location.href='add_competence.py'">Add competence</button>
      User: {{username}}
    </div>
    <hr>
    <h1>Competence Matrix</h1>
    <table style="font-size=14">
    % n=0
    % for row in rowscale:
    %   if n%2==0:
    %     if n>0:
            </tr>
    %       end
          <tr>
    %     end
        <td class="td_scale{{row['id']}}">{{row['name']}}</td>
    %   n=n+1
    %   end
    </table>
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
          <tr><td><a href="competence.py?competence_id={{row['competence_id']}}">{{row['competence']}}</a></td>
    %     comp=row['competence']
    %     end
    %   if row['scale_id'] is None:
          <td class="td_scale0">&nbsp;?&nbsp;</td>
    %   else:
          <td class="td_scale{{row['scale_id']}}">&nbsp;&nbsp;&nbsp;&nbsp;</td>
    %     end
    %   end
    </table>
  </body>
</html>
