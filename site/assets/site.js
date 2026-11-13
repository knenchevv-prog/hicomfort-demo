(function(){
  var HC=window.HC||{};
  var $=function(s,r){return (r||document).querySelector(s)}, $$=function(s,r){return [].slice.call((r||document).querySelectorAll(s))};
  var rm=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;

  // mobile menu
  var burger=$('#burger'), drawer=$('#drawer');
  if(burger)burger.addEventListener('click',function(){var o=drawer.classList.toggle('open');burger.setAttribute('aria-expanded',o)});

  // logo curtain between pages
  var veil=$('#veil'), vsec=$('#veil-sec');
  if(veil){
    veil.addEventListener('animationend',function(e){if(e.animationName==='lift')veil.classList.remove('boot')});
    window.addEventListener('pageshow',function(e){if(e.persisted){veil.classList.remove('on');veil.classList.remove('boot')}});
    $$('a[data-nav]').forEach(function(a){a.addEventListener('click',function(e){
      if(rm||e.metaKey||e.ctrlKey||e.shiftKey||e.altKey||e.button)return;
      e.preventDefault();
      vsec.textContent=a.getAttribute('data-nav');
      veil.classList.remove('boot');veil.classList.add('on');
      try{sessionStorage.setItem('hc-nav','1')}catch(_){}
      setTimeout(function(){window.location.href=a.href},950);
    })});
  }

  // colour themes
  var G='226,188,102';
  function readG(){var v=getComputedStyle(document.documentElement).getPropertyValue('--glow-rgb').trim();if(v)G=v}
  function gl(a){return 'rgba('+G+','+a+')'}
  function setTheme(th){var de=document.documentElement;if(th)de.setAttribute('data-th',th);else de.removeAttribute('data-th');
    $$('#themes button').forEach(function(b){b.setAttribute('aria-pressed',b.dataset.th===th)});readG();
    try{localStorage.setItem('hc-theme',th)}catch(_){}}
  var themes=$('#themes');
  if(themes){
    themes.addEventListener('click',function(e){var b=e.target.closest('button');if(b)setTheme(b.dataset.th)});
    var saved='';try{saved=localStorage.getItem('hc-theme')||''}catch(_){}
    setTheme(saved&&$('#themes button[data-th="'+saved+'"]')?saved:'');
  }

  // floor plan
  var chips=$('#chips');
  if(chips&&HC.rooms){
    var rooms=HC.rooms;
    Object.keys(rooms).forEach(function(k){var b=document.createElement('button');b.className='chip';b.type='button';b.dataset.room=k;b.textContent=rooms[k].n;chips.appendChild(b)});
    var pick=function(k){
      $$('.room').forEach(function(g){g.classList.toggle('on',g.dataset.room===k)});
      $$('.chip',chips).forEach(function(c){c.setAttribute('aria-pressed',c.dataset.room===k)});
      $('#room-title').textContent=rooms[k].t;
      $('#room-list').innerHTML=rooms[k].l.map(function(x){return '<li>'+x+'</li>'}).join('');
    };
    $$('.room').forEach(function(g){
      g.addEventListener('click',function(){pick(g.dataset.room)});
      g.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();pick(g.dataset.room)}});
    });
    chips.addEventListener('click',function(e){var b=e.target.closest('.chip');if(b)pick(b.dataset.room)});
    pick('hol');
  }

  // before / after: moves only while the round handle is held
  var ba=$('#ba');
  if(ba){
    var bar=$('#ba-range'), knob=$('#ba-knob'), dragging=false;
    var setPos=function(p){p=Math.max(0,Math.min(100,p));ba.style.setProperty('--pos',p+'%');bar.value=p;knob.setAttribute('aria-valuenow',Math.round(p))};
    var fromEvent=function(e){var r=ba.getBoundingClientRect();setPos((e.clientX-r.left)/r.width*100)};
    knob.addEventListener('pointerdown',function(e){dragging=true;e.preventDefault();try{knob.setPointerCapture(e.pointerId)}catch(_){ }});
    knob.addEventListener('pointermove',function(e){if(dragging)fromEvent(e)});
    ['pointerup','pointercancel','lostpointercapture'].forEach(function(n){knob.addEventListener(n,function(){dragging=false})});
    knob.addEventListener('keydown',function(e){if(e.key==='ArrowLeft')setPos(+bar.value-5);if(e.key==='ArrowRight')setPos(+bar.value+5)});
  }

  // moving drawings behind dark bands: one per page
  function ez(v){return v<.5?4*v*v*v:1-Math.pow(-2*v+2,3)/2}
  var scenes={
    tape:function(x,w,h,t){
      var g=48,o=t%g,i,j;
      x.strokeStyle='rgba(255,255,255,.055)';x.lineWidth=1;x.beginPath();
      for(i=-g;i<w+g;i+=g){x.moveTo(i+o,0);x.lineTo(i+o,h)}
      for(j=0;j<h;j+=g){x.moveTo(0,j);x.lineTo(w,j)}
      x.stroke();
      var s=12,run=t*1.5,off=run%(s*10),n0=Math.floor(run/(s*10)),k,px,m;
      x.strokeStyle=gl(.75);x.fillStyle=gl(.85);x.font='10px "JetBrains Mono",monospace';x.beginPath();
      for(k=0;k<w/s+12;k++){px=k*s-off;m=k%10===0?22:(k%5===0?14:8);x.moveTo(px,h);x.lineTo(px,h-m);if(k%10===0)x.fillText(((n0+k/10)*10)+' cm',px+4,h-27)}
      x.stroke();
    },
    tiles:function(x,w,h,t){
      var s=w<700?46:62,cols=Math.ceil(w/s),rows=Math.ceil(h/s),N=cols*rows,cyc=(t*N/300)%(N*1.3),fade=cyc>N?1-(cyc-N)/(N*.3):1,r,c,ord,age,k;
      x.lineWidth=1;
      for(r=0;r<rows;r++)for(c=0;c<cols;c++){
        ord=(rows-1-r)*cols+c;if(ord>=cyc)continue;age=cyc-ord;k=(.3+.7*c/cols)*fade;
        x.fillStyle=gl((.04+(age<8?(8-age)/8*.42:0))*k);x.fillRect(c*s+3,h-(rows-r)*s+3,s-6,s-6);
        x.strokeStyle=gl(.2*k);x.strokeRect(c*s+3.5,h-(rows-r)*s+3.5,s-7,s-7);
      }
    },
    steps:function(x,w,h,t){
      var T=t/24,y=h-30,x0=w*.07,x1=w*.93,seg=1.25,dw=.6,st=seg+dw,run=4*st,cyc=run+3.5,u=T%cyc,i=0,f=0,q,A=Math.min(1,u/.6),pulse=-1,pf=0,n,nx,lit;
      if(u<run){i=Math.floor(u/st);f=u-i*st;q=(i+ez(Math.min(f/seg,1)))/4;if(f>seg){pulse=i+1;pf=(f-seg)/dw}else if(i===0&&f<.5){pulse=0;pf=f/.5}}
      else{q=1;if(u>run+2.6)A=Math.max(0,1-(u-run-2.6)/.8)}
      x.lineWidth=2;x.strokeStyle='rgba(255,255,255,.14)';x.beginPath();x.moveTo(x0,y);x.lineTo(x1,y);x.stroke();
      x.strokeStyle=gl(.9*A);x.beginPath();x.moveTo(x0,y);x.lineTo(x0+(x1-x0)*q,y);x.stroke();
      x.font='11px "JetBrains Mono",monospace';x.textAlign='center';
      for(n=0;n<5;n++){nx=x0+(x1-x0)*n/4;lit=q>=n/4-.001;
        x.beginPath();x.arc(nx,y,lit?6+A:5,0,6.3);x.fillStyle='rgb(22,26,30)';x.fill();
        if(lit){x.fillStyle=gl(A);x.fill()}
        x.strokeStyle=gl(lit?.45+.55*A:.45);x.stroke();
        x.fillStyle=gl(lit?.4+.55*A:.4);x.fillText('0'+(n+1),nx,y-18)}
      x.textAlign='left';
      if(pulse>=0){x.beginPath();x.arc(x0+(x1-x0)*pulse/4,y,7+ez(pf)*17,0,6.3);x.strokeStyle=gl((1-pf)*.65*A);x.stroke()}
      if(u<run&&f<=seg){x.beginPath();x.arc(x0+(x1-x0)*q,y,11,0,6.3);x.fillStyle=gl(.2);x.fill()}
    },
    plan:function(x,w,h,t){
      var small=w<700,bw=small?w-40:Math.min(w*.4,460),bh=small?h-36:Math.min(h-64,170),bx=small?20:w-bw-48,by=(h-bh)/2,al=small?.22:.62;
      var S=[[0,0,1,0],[1,0,1,1],[1,1,0,1],[0,1,0,0],[.42,0,.42,.62],[.42,.62,1,.62],[.7,.62,.7,1],[0,.62,.22,.62],[.3,.62,.42,.62]];
      var tot=0,L,i,a,len,d;S.forEach(function(a){tot+=Math.hypot((a[2]-a[0])*bw,(a[3]-a[1])*bh)});
      var u=(t%520)/520,A=u>.88?Math.max(0,1-(u-.88)/.12):1;al*=A;L=ez(Math.min(u*1.45,1))*tot;
      x.strokeStyle=gl(al);x.lineWidth=2;x.lineCap='square';x.beginPath();
      for(i=0;i<S.length&&L>0;i++){a=S[i];len=Math.hypot((a[2]-a[0])*bw,(a[3]-a[1])*bh);d=Math.min(L/len,1);
        x.moveTo(bx+a[0]*bw,by+a[1]*bh);x.lineTo(bx+(a[0]+(a[2]-a[0])*d)*bw,by+(a[1]+(a[3]-a[1])*d)*bh);L-=len}
      x.stroke();x.lineCap='butt';
      if(L>=0&&!small){x.fillStyle=gl(.8*A);x.font='10px "JetBrains Mono",monospace';x.fillText(HC.dim||'11,40 m',bx+bw/2-22,by+bh+18);
        x.strokeStyle=gl(.5*A);x.lineWidth=1;x.beginPath();x.moveTo(bx,by+bh+8);x.lineTo(bx+bw,by+bh+8);x.stroke()}
    },
    // a spirit level: the bubble swings and settles in the middle
    level:function(x,w,h,t){
      var T=t/24,cyc=7.5,u=T%cyc,A=Math.min(1,u/.5),small=w<700;
      if(u>cyc-.8)A=Math.max(0,(cyc-u)/.8);
      var bw=small?w-48:Math.min(w*.42,520),bh=26,bx=small?24:w-bw-48,by=h-58,cx=bx+bw/2,cy=by+bh/2,vw=Math.min(150,bw*.4),i;
      var off=Math.exp(-u*.75)*Math.cos(u*3.6),k=small?.5:1;
      x.lineWidth=2;x.strokeStyle=gl(.5*A*k);x.strokeRect(bx,by,bw,bh);
      x.lineWidth=1;x.beginPath();
      for(i=bx+16;i<bx+bw-8;i+=16){if(Math.abs(i-cx)<vw/2+10)continue;x.moveTo(i,by+bh);x.lineTo(i,by+bh-6)}
      x.stroke();
      x.lineWidth=2;x.strokeStyle=gl(.8*A*k);x.strokeRect(cx-vw/2,by+5,vw,bh-10);
      x.beginPath();x.moveTo(cx-15,by+5);x.lineTo(cx-15,by+bh-5);x.moveTo(cx+15,by+5);x.lineTo(cx+15,by+bh-5);x.stroke();
      x.beginPath();x.ellipse(cx+off*(vw/2-16),cy,12,6,0,0,6.3);x.fillStyle=gl((Math.abs(off)<.04?.95:.6)*A*k);x.fill();
    }
  };
  $$('canvas.tape').forEach(function(c){
    var x=c.getContext('2d'),t=0,last=null,w=0,h=0,d=Math.min(window.devicePixelRatio||1,2),on=false,draw=scenes[c.dataset.kind||'tape'];
    function size(){w=c.clientWidth;h=c.clientHeight;c.width=Math.round(w*d);c.height=Math.round(h*d);x.setTransform(d,0,0,d,0,0)}
    function frame(ts){
      if(!on)return;
      if(last===null)last=ts;
      t+=Math.min((ts-last)/1000,.05)*24;last=ts;
      x.clearRect(0,0,w,h);draw(x,w,h,t);
      requestAnimationFrame(frame);
    }
    size();window.addEventListener('resize',size);
    if(rm){draw(x,w,h,400);return}
    if(!('IntersectionObserver' in window)){on=true;requestAnimationFrame(frame);return}
    new IntersectionObserver(function(en){var was=on;on=en[0].isIntersecting;if(on&&!was){size();last=null;requestAnimationFrame(frame)}}).observe(c);
  });

  // scroll reveal
  if('IntersectionObserver' in window&&!rm){
    var io=new IntersectionObserver(function(en){en.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px'});
    $$('.pg .head,.card,.g,.step,.calc,.rev,.ba,details,form').forEach(function(el,i){el.classList.add('rv');el.style.transitionDelay=(i%4*70)+'ms';io.observe(el)});
  }

  // gallery
  var gal=$('#gal'), lb=$('#lb');
  if(gal&&HC.items){
    var items=HC.items, cats=HC.cats;
    items.forEach(function(it,i){
      var b=document.createElement('button');b.className='tile '+it.m;b.type='button';b.dataset.c=it.c;b.dataset.i=i;
      b.innerHTML='<span class="cap"><small>'+cats[it.c]+'</small>'+it.t+'</span>';gal.appendChild(b);
    });
    gal.addEventListener('click',function(e){
      var b=e.target.closest('.tile');if(!b)return;var it=items[b.dataset.i];
      $('#lb-img').className='lb-img '+it.m;$('#lb-title').textContent=it.t;$('#lb-text').textContent=it.d;
      if(lb.showModal)lb.showModal();else lb.setAttribute('open','');
    });
    $('#lb-close').addEventListener('click',function(){lb.close()});
    lb.addEventListener('click',function(e){if(e.target===lb)lb.close()});
    $('#filters').addEventListener('click',function(e){
      var b=e.target.closest('.chip');if(!b)return;
      $$('.chip',this).forEach(function(c){c.setAttribute('aria-pressed',c===b)});
      $$('.tile',gal).forEach(function(t){t.hidden=!(b.dataset.f==='all'||t.dataset.c===b.dataset.f)});
    });
  }

  // calculator
  var area=$('#area'), lvl=$('#lvl');
  if(area&&lvl){
    var num=function(n){return (Math.round(n/100)*100).toLocaleString(HC.locale||'bg-BG')};
    var range=function(lo,hi){return HC.lang==='en'?'€'+num(lo)+' – €'+num(hi):num(lo)+' – '+num(hi)+' €'};
    var cur=[0,0],raf=0,priceEl=$('#price');
    var glide=function(lo,hi){
      priceEl.dataset.final=range(lo,hi);
      if(rm||!cur[1]){cur=[lo,hi];priceEl.textContent=priceEl.dataset.final;return}
      var from=cur.slice(),t0=null;cancelAnimationFrame(raf);
      raf=requestAnimationFrame(function step(ts){if(t0===null)t0=ts;var k=Math.min((ts-t0)/450,1),e=1-Math.pow(1-k,3);
        cur=[from[0]+(lo-from[0])*e,from[1]+(hi-from[1])*e];priceEl.textContent=range(cur[0],cur[1]);
        if(k<1)raf=requestAnimationFrame(step)});
    };
    var calc=function(instant){
      var a=+area.value, b=$('button[aria-pressed="true"]',lvl);
      $('#area-out').textContent=a;$('#k-area').textContent=a;
      if(instant===true){cancelAnimationFrame(raf);cur=[a*b.dataset.min,a*b.dataset.max];priceEl.dataset.final=range(cur[0],cur[1]);priceEl.textContent=priceEl.dataset.final}
      else glide(a*b.dataset.min,a*b.dataset.max);
      $('#lvl-desc').textContent=b.dataset.desc;
    };
    area.addEventListener('input',function(){calc(true)});
    lvl.addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;$$('button',lvl).forEach(function(x){x.setAttribute('aria-pressed',x===b)});calc()});
    // carry the estimate over to the contact page
    $('#to-offer').addEventListener('click',function(){
      var b=$('button[aria-pressed="true"]',lvl);
      var msg=HC.offer.replace('{type}',b.textContent.toLowerCase()).replace('{area}',area.value).replace('{price}',priceEl.dataset.final);
      try{sessionStorage.setItem('hc-offer',JSON.stringify({area:area.value,msg:msg}))}catch(_){}
    });
    calc();
  }

  // contact form (demo only: nothing is sent)
  var form=$('#form');
  if(form){
    try{var o=JSON.parse(sessionStorage.getItem('hc-offer')||'null');if(o){$('#f-area').value=o.area;$('#f-msg').value=o.msg;sessionStorage.removeItem('hc-offer')}}catch(_){}
    form.addEventListener('submit',function(e){
      e.preventDefault();var m=$('#form-msg');
      if(!$('#f-name').value.trim()||!$('#f-tel').value.trim()){m.textContent=HC.formMissing;m.classList.add('show');return}
      m.textContent=HC.formDemo;m.classList.add('show');
    });
  }
})();
