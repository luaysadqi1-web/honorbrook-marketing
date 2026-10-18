/* Honorbrook calculators — everything runs in the browser; nothing is stored or sent. */
(function(){
  function num(id,f){ var el=f.querySelector('#'+id); if(!el) return 0; var v=parseFloat(String(el.value).replace(/[^0-9.\-]/g,'')); return isNaN(v)?0:v; }
  var USD0=new Intl.NumberFormat('en-US',{style:'currency',currency:'USD',maximumFractionDigits:0});
  var USD2=new Intl.NumberFormat('en-US',{style:'currency',currency:'USD',minimumFractionDigits:2,maximumFractionDigits:2});
  function m0(x){ return USD0.format(Math.round(x)); }
  function m2(x){ return USD2.format(x); }
  function row(l,v,b){ return '<tr'+(b?' class="tot"':'')+'><th scope="row">'+l+'</th><td>'+v+'</td></tr>'; }
  function big(label,val,note){ return '<div class="calc-big"><span class="calc-big-l">'+label+'</span><span class="calc-big-v">'+val+'</span>'+(note?'<span class="calc-big-n">'+note+'</span>':'')+'</div>'; }
  function tbl(rows){ return '<table class="calc-tbl"><tbody>'+rows.join('')+'</tbody></table>'; }

  var CALCS={
    life:function(f){
      var inc=num('inc',f),yrs=num('yrs',f),mort=num('mort',f),debt=num('debt',f),kids=num('kids',f),edu=num('edu',f),fin=num('fin',f),cov=num('cov',f),sav=num('sav',f);
      var replace=inc*yrs, college=kids*edu, need=replace+mort+debt+college+fin, have=cov+sav, gap=Math.max(0,need-have);
      return big('Estimated additional coverage to consider',m0(gap), gap===0?'Your existing coverage and savings may already meet this estimate. An agent can double-check.':'This is the gap between what your family could need and what you already have.')+
        tbl([row('Income to replace ('+yrs+' years)',m0(replace)),row('Mortgage',m0(mort)),row('Other debts',m0(debt)),row('College ('+kids+' child'+(kids===1?'':'ren')+')',m0(college)),row('Final expenses',m0(fin)),row('Total need',m0(need),1),row('Minus existing coverage and savings','&minus;'+m0(have)),row('Gap',m0(gap),1)]);
    },
    ichra:function(f){
      var n=num('emp',f),prem=num('grp',f),pct=num('pct',f),allow=num('allow',f),fee=num('fee',f);
      if(n<=0) return '<p class="calc-err">Enter the number of employees.</p>';
      var grp=prem*pct/100*n*12, ich=(allow+fee)*n*12, diff=grp-ich;
      var msg=diff>0?'The allowance would cost about '+m0(diff)+' less per year, or '+m0(diff/n/12)+' per employee per month.':diff<0?'The allowance would cost about '+m0(-diff)+' more per year, or '+m0(-diff/n/12)+' per employee per month.':'The two options cost about the same.';
      return big('Estimated yearly cost: group plan vs. ICHRA / CHOICE',m0(grp)+' vs. '+m0(ich),msg)+
        tbl([row('Group plan: your share of premiums',m0(grp)),row('ICHRA / CHOICE: allowances',m0(allow*n*12)),row('ICHRA / CHOICE: administration fees',m0(fee*n*12)),row('ICHRA / CHOICE total',m0(ich),1),row('Difference (group minus ICHRA)',(diff>=0?'':'&minus;')+m0(Math.abs(diff)),1)])+
        '<p class="calc-note">Employees choose and own their own plans with an ICHRA, so their out-of-pocket costs and plan choice can differ from a group plan.</p>';
    },
    medicare:function(f){
      var plan=f.querySelector('#plan').value, prem=num('prem',f), pd=num('pd',f), moop=num('moop',f);
      var B=202.90, annual=(B+prem+pd)*12;
      var rows=[row('Part B premium (standard, 2026)',m2(B*12)+' / yr')];
      if(plan!=='orig') rows.push(row(plan==='ma'?'Medicare Advantage plan premium':'Medigap premium',m2(prem*12)+' / yr'));
      rows.push(row('Part D premium',m2(pd*12)+' / yr')); rows.push(row('Estimated yearly premiums',m2(annual),1));
      var exp;
      if(plan==='orig') exp='<p class="calc-note"><strong>If you have a heavy-use year:</strong> you would also pay the $283 Part B deductible, 20% of most outpatient costs with <strong>no yearly cap</strong>, and a $1,736 Part A deductible for each hospital benefit period (2026). Many people add a Medigap or Advantage plan to limit this.</p>';
      else if(plan==='medigap') exp='<p class="calc-note"><strong>If you have a heavy-use year:</strong> most Medigap plans limit your extra costs to the $283 Part B deductible plus any copays your specific plan has. Part D drugs have their own rules.</p>';
      else exp='<p class="calc-note"><strong>If you have a heavy-use year:</strong> '+(moop>0?'your in-network costs for covered services are capped at your plan&rsquo;s out-of-pocket maximum of '+m0(moop)+', for a possible total of about '+m0(annual+moop)+' for the year.':'your costs for covered in-network services are capped at your plan&rsquo;s out-of-pocket maximum. Enter it above to see a total.')+' Drugs, out-of-network care and some services may not count toward the cap.</p>';
      return big('Estimated yearly premiums',m2(annual),'About '+m2(annual/12)+' per month before any copays or deductibles.')+tbl(rows)+exp+
        '<p class="calc-note">Standard 2026 amounts. Higher-income enrollees pay more for Parts B and D. See Medicare.gov for your exact figures.</p>';
    },
    aca:function(f){
      var hh=Math.max(1,Math.round(num('hh',f))), magi=num('magi',f), bench=num('bench',f);
      if(magi<=0||bench<=0) return '<p class="calc-err">Enter your household income and the benchmark premium.</p>';
      var fpl=15960+5680*(hh-1), ratio=magi/fpl*100;
      var head='<p class="calc-note">Poverty guideline for '+hh+' '+(hh===1?'person':'people')+': '+m0(fpl)+'. Your income is about '+Math.round(ratio)+'% of it.</p>';
      if(ratio<100) return head+'<p class="calc-note"><strong>Below 100% of poverty</strong>, you generally do not qualify for marketplace premium tax credits. You may qualify for Medicaid or other help depending on your state. Call us and we will point you the right way.</p>';
      if(ratio>400) return big('Estimated premium tax credit','$0','Households above 400% of poverty do not qualify under current rules.')+head+'<p class="calc-note">You would pay full price: about '+m0(bench)+' per month for the benchmark plan. Some states and plans offer other savings.</p>';
      var B=[[0,133,2.15,2.15],[133,150,3.23,4.3],[150,200,4.3,6.78],[200,250,6.78,8.66],[250,300,8.66,10.22],[300,400,10.22,10.22]], pct=10.22;
      for(var i=0;i<B.length;i++){ var b=B[i]; if(ratio<b[1]||i===B.length-1){ pct=b[2]+(b[3]-b[2])*Math.max(0,Math.min(1,(ratio-b[0])/(b[1]-b[0]))); break; } }
      var contrib=magi*pct/100/12, credit=Math.max(0,bench-contrib);
      var medicaid=ratio<138?'<p class="calc-note">At this income you may qualify for Medicaid in a state that expanded it, such as Virginia. Check eligibility before choosing a marketplace plan.</p>':'';
      return big('Estimated monthly premium tax credit',m0(credit),'Applied against the benchmark premium of '+m0(bench)+' per month.')+
        tbl([row('Required contribution rate (2027 IRS table)',pct.toFixed(2)+'%'),row('You pay for the benchmark plan',m0(contrib)+' / mo'),row('Credit',m0(credit)+' / mo',1),row('Credit per year',m0(credit*12))])+head+medicaid+
        '<p class="calc-note">You can use the credit toward any marketplace plan; a cheaper plan lowers what you pay. Estimates only; your credit is reconciled on your tax return.</p>';
    },
    retire:function(f){
      var age=num('age',f), rage=num('rage',f), bal=num('bal',f), mo=num('mo',f), ret=num('ret',f), need=num('need',f), ss=num('ss',f);
      var n=rage-age; if(n<=0) return '<p class="calc-err">Your retirement age needs to be later than your current age.</p>';
      var r=Math.pow(1+ret/100,1/12)-1, m=n*12, g=Math.pow(1+r,m), af=r===0?m:(g-1)/r;
      var fv=bal*g+mo*af, income=fv*0.04/12, total=income+ss, gap=need-total;
      var msg, extra='';
      if(gap<=0) msg='On these numbers you are on track: your projected income is about '+m0(total)+' a month against a goal of '+m0(need)+'.';
      else{ var add=gap*12/0.04/af; msg='You may be about '+m0(gap)+' a month short of your goal.'; extra='<p class="calc-note">Saving roughly <strong>'+m0(add)+' more per month</strong> from now until retirement would close that gap on these assumptions.</p>'; }
      return big('Projected savings at age '+rage,m0(fv),msg)+
        tbl([row('Years until retirement',String(n)),row('Monthly income from savings (4% rule)',m0(income)),row('Social Security and pension',m0(ss)),row('Total monthly income',m0(total),1),row('Your monthly goal',m0(need)),row(gap>0?'Shortfall':'Surplus',m0(Math.abs(gap)),1)])+extra+
        '<p class="calc-note">Results are in today&rsquo;s dollars and assume steady growth. Real markets go up and down, and taxes are not included.</p>';
    }
  };

  function run(f){
    var k=f.getAttribute('data-calc'), out=f.querySelector('.calc-out');
    try{ out.innerHTML=CALCS[k](f); }catch(e){ out.innerHTML='<p class="calc-err">Something went wrong. Please check your numbers.</p>'; return; }
    if(typeof window.gtag==='function'){ try{ window.gtag('event','calculator_use',{calculator:k}); }catch(e){} }
  }
  document.querySelectorAll('form[data-calc]').forEach(function(f){
    f.querySelector('.calc-go').addEventListener('click',function(){ run(f); });
    f.addEventListener('keydown',function(e){ if(e.key==='Enter'&&e.target.tagName!=='BUTTON'){ e.preventDefault(); run(f); } });
    f.querySelectorAll('input[data-kind=money]').forEach(function(i){
      i.addEventListener('blur',function(){ var v=parseFloat(i.value.replace(/[^0-9.\-]/g,'')); if(!isNaN(v)) i.value=v.toLocaleString('en-US'); });
      i.addEventListener('focus',function(){ i.value=i.value.replace(/,/g,''); });
    });
  });
})();
