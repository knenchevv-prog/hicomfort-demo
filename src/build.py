#!/usr/bin/env python3
"""Builds the HI Comfort demo site (Bulgarian + English, one page per section) into ../site.

Run:  python3 src/build.py
Edit texts in T below, styles in site.css, behaviour in site.js. Never edit ../site by hand.
"""
import json, os, shutil

SRC = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(SRC), "site")
read = lambda n: open(os.path.join(SRC, n), encoding="utf-8").read().strip("\n")

PHONE_TEL, PHONE = "+359898643973", "089 864 3973"
EMAIL = "hicomfort2016@gmail.com"
MAPS = "https://www.google.com/maps/search/?api=1&query=HI+Comfort+%D0%92%D0%B0%D1%80%D0%BD%D0%B0&query_place_id=ChIJrxdjM15VpEAR5QzasNsiq5w"
FACEBOOK = "https://www.facebook.com/profile.php?id=61586625354948"

PAGES = ["home", "services", "projects", "prices", "process", "faq", "contact"]
FILES = {
    "bg": dict(home="index.html", services="uslugi.html", projects="proekti.html", prices="ceni.html",
               process="kak-rabotim.html", faq="vaprosi.html", contact="kontakti.html"),
    "en": dict(home="index.html", services="services.html", projects="projects.html", prices="prices.html",
               process="how-we-work.html", faq="faq.html", contact="contact.html"),
}

T = {
"bg": dict(
    html_lang="bg", locale="bg-BG", dim="11,40 m", other="en", other_label="EN", other_name="English",
    ribbon="ДЕМО КОНЦЕПЦИЯ ЗА HI COMFORT · цените, условията и илюстрациите са примерни",
    logo_sub="РЕМОНТИ · ВАРНА", logo_aria="HI Comfort начало", menu_aria="Основно меню", burger="Отвори менюто",
    slogan="Комфортът за Вас, ремонтът от нас",
    nav=dict(home="Начало", services="Услуги", projects="Проекти", prices="Цени", process="Как работим", faq="Въпроси", contact="Контакти"),
    title=dict(home="HI Comfort демо сайт", services="Услуги · HI Comfort", projects="Проекти · HI Comfort", prices="Цени · HI Comfort",
               process="Как работим · HI Comfort", faq="Въпроси · HI Comfort", contact="Контакти · HI Comfort"),
    footer_l="HI Comfort · цялостни ремонти и довършителни работи · Варна", footer_r="Демо концепция, не е официалният сайт на фирмата",
    mbar=("Бързи действия", "Обади се", "Viber", "Оферта"), themes_aria="Цветова схема (само в демото)", themes_label="Цвят",
    # home
    rating="оценка в Google ›", hero_eyebrow="Цялостни ремонти и довършителни работи · Варна",
    hero_h=("Комфортът за Вас,", "ремонтът от нас."),
    hero_lead="Поемаме ремонта на Вашия дом от първия оглед до последната лайсна. Един екип, една оферта, един човек, който отговаря за всичко.",
    cta_visit="Заяви оглед", cta_calc="Изчисли ориентировъчна цена", tel_line=("Или се обадете:", "Пон–Съб"),
    plan_aria="Интерактивен план на апартамент", plan_top="План · примерен апартамент",
    proof=(("5,0 ★", "виж отзивите в Google"), ("283", "последователи във Facebook"), ("Пон–Съб", "работим шест дни, заяви оглед")),
    home_srv=("Услуги", "Всичко за дома.", "От един изпълнител."), all_services="Всички услуги",
    ba_head=("Преди и след", "Хванете кръга и плъзнете.", "Разликата се вижда сама."),
    ba_note="Илюстрация за демото. Тук идват реалните снимки преди и след от обектите на HI Comfort.",
    all_projects="Виж всички проекти",
    g_head=("Какво получавате", "Обещания на хартия.", "Не само на думи."),
    g=(("€", "Цена, записана в офертата", "Знаете сумата преди да започнем. Промяна има само ако Вие поискате нещо допълнително."),
       ("1", "Един човек за връзка", "Не гоните майстори по телефона. Един отговорник знае всичко за обекта."),
       ("◷", "Срок по график", "Виждате етапите предварително и кога приключва всеки от тях."),
       ("✓", "Чисто предаване", "Извозваме отпадъците и предаваме жилището готово за нанасяне.")),
    g_note="Предложение за текстове. Условията се потвърждават от собственика преди пускане на сайта.",
    rev=("Клиентите ни оценяват с пет звезди в Google", "Прочетете какво казват хората, на които вече сме направили ремонт, и вижте още обекти във Facebook.",
         "Отзиви в Google", "Facebook страница", "5 от 5 звезди"),
    band=("Готови ли сте за оглед?", "Идваме на място, мерим и Ви даваме писмена оферта.", "Заяви оглед"),
    # services
    srv_head=("Услуги", "Всичко за дома.", "От един изпълнител.", "Изберете една услуга или ни оставете целия ремонт."),
    srv_main="ОСНОВНА УСЛУГА", srv_cta="Искам оферта",
    srv=(("Цялостен ремонт на апартамент", "Къртене, инсталации, замазки, шпакловка, настилки, врати и боя. Вие говорите с един човек, а ние координираме всички майстори."),
         ("Ремонт на баня", "Хидроизолация, нови ВиК и ел. инсталации, плочки и монтаж на санитария."),
         ("Кухня", "Изводи за уредите, плочки на гръб и под, подготовка за шкафовете."),
         ("Подови настилки", "Ламинат, гранитогрес и паркет с подготовка на основата."),
         ("Шпакловка и боядисване", "Равни стени и тавани, гипсокартон, декоративни мазилки."),
         ("Дограма и врати", "Съвет при избора, монтаж и обръщане около отворите."),
         ("Ел. и ВиК инсталации", "Нови трасета, табла, контакти и осветление по проект.")),
    # projects
    prj_head=("Проекти", "Завършени обекти.", "Разгледайте по помещение.", ""),
    filters=("Всички", "Бани", "Кухни", "Дневни и спални"),
    prj_note="Плочките показват материали вместо снимки. В готовия сайт всяка отваря галерия от реалния обект.",
    lb_close="Затвори", lb_note="Място за снимки от реалния обект.",
    cats=dict(bath="Баня", kitchen="Кухня", living="Дневна и спалня"),
    items=(("Баня с едроформатен гранитогрес", "Нови инсталации, хидроизолация, плочи с мраморен рисунък и месингови акценти."),
           ("Дневна с дъбов паркет", "Изравняване на основата, паркет рибена кост, первази и боя."),
           ("Кухня с плочки на гръб", "Преместени изводи за уредите, плочки на гръб и под."),
           ("Баня в тъмен камък", "Душ зона на едно ниво с пода, линеен сифон, скрито казанче."),
           ("Спалня с декоративна мазилка", "Гладки стени, декоративна мазилка зад леглото, ново осветление."),
           ("Кухня с терацо под", "Под от терацо плочи, нова ел. инсталация, окачен таван."),
           ("Дневна с цветна стена", "Шпакловка, боядисване в два цвята, ламинат и интериорни врати."),
           ("Кухненски кът с тухла", "Декоративна тухла, изводи за остров и нова настилка.")),
    # prices
    prc_head=("Ориентировъчна цена", "Колко ще струва?", "Сметнете за 10 секунди.", ""),
    area_label="Квадратура на жилището", lvl_label="Вид ремонт",
    lvl=(("Освежаване", "Шпакловка на места, боядисване и дребни поправки."),
         ("Основен", "Нови инсталации, замазки, настилки, шпакловка и боя."),
         ("До ключ", "Основен ремонт плюс бани, врати, осветление и довършване до нанасяне.")),
    k_for="Ориентировъчно за", exact="Искам точна оферта", prc_note="Примерни стойности за демото. Реалните цени се задават от HI Comfort.",
    offer="Интересувам се от {type} ремонт на {area} m². Ориентировъчно: {price}.",
    # process
    prs_head=("Как работим", "Пет стъпки.", "Без изненади по пътя.", ""),
    steps=(("Оглед", "Идваме на място, мерим и чуваме какво искате."), ("Оферта", "Получавате писмена оферта по дейности, материали и срок."),
           ("Договор", "Записваме цена, срок и етапи на плащане."), ("Ремонт", "Работим по график и Ви показваме напредъка."),
           ("Предаване", "Почистваме и минаваме заедно през всяко помещение.")),
    # faq
    faq_head=("Чести въпроси", "Преди да се обадите.", "Кратки отговори.", ""),
    faq=(("Колко време отнема ремонтът?", "Зависи от квадратурата и дейностите. Срокът се записва в офертата след огледа, за да знаете датата предварително."),
         ("Мога ли да живея в жилището по време на ремонта?", "При частичен ремонт често е възможно. При основен ремонт препоръчваме жилището да е свободно. Обсъждаме го на огледа."),
         ("Вие ли купувате материалите?", "Можем да поемем доставката или да работим с избрани от Вас материали. Помагаме с избора на настилки, плочки и дограма."),
         ("Как се плаща?", "На етапи, описани в договора. Плащате за завършена работа, а не всичко предварително."),
         ("Работите ли извън Варна?", "Работим във Варна и региона. Обадете се и ще кажем дали поемаме Вашия адрес.")),
    # contact
    ct_head=("Контакти", "Заявете оглед.", "Отговаряме в рамките на деня."),
    ct_rows=(("Телефон и Viber", None), ("Имейл", None), ("Адрес", "ул. „Цар Асен I“ 25, Варна"), ("Работно време", "Пон–Пет 8:00–18:00 · Съб 9:00–18:00")),
    ct_map="Виж в Google Maps", form_h="Запитване за оферта",
    f=("Име", "Телефон", "Вид ремонт", "Квадратура (m²)", "Какво искате да направим?", "Изпрати запитване"),
    f_types=("Цялостен ремонт", "Баня", "Кухня", "Настилки", "Шпакловка и боя", "Друго"),
    form_missing="Попълнете име и телефон, за да можем да се свържем с Вас.",
    form_demo="Това е демо и запитването не е изпратено. В готовия сайт то пристига директно при HI Comfort по имейл и Viber.",
    # floor plan + before/after
    rooms=dict(
        hol=("Хол", "24 m²", ("Шпакловка и боядисване на стени и таван", "Ламинат или паркет с первази", "Окачен таван и скрито осветление", "Интериорни врати")),
        kuhnya=("Кухня", "12 m²", ("Ел. и ВиК изводи за всички уреди", "Плочки на гръб и под", "Подготовка на стените за шкафовете")),
        banya=("Баня", "5 m²", ("Хидроизолация на под и стени", "Нови ВиК и ел. инсталации", "Гранитогрес и фаянс", "Монтаж на санитария и аксесоари")),
        koridor=("Коридор", "6 m²", ("Ново ел. табло и трасета", "Настилка, устойчива на износване", "Обръщане около входната врата")),
        spalnya=("Спалня", "16 m²", ("Изравняване на стените", "Подова настилка и первази", "Боядисване в избран цвят", "Врата и осветление")),
        terasa=("Тераса", "8 m²", ("Усвояване и остъкляване", "Топлоизолация", "Настилка за външни условия"))),
    svg={},
),
"en": dict(
    html_lang="en", locale="en-GB", dim="11.40 m", other="bg", other_label="BG", other_name="Български",
    ribbon="DEMO CONCEPT FOR HI COMFORT · prices, terms and illustrations are examples",
    logo_sub="RENOVATIONS · VARNA", logo_aria="HI Comfort home", menu_aria="Main menu", burger="Open the menu",
    slogan="Your comfort, our renovation",
    nav=dict(home="Home", services="Services", projects="Projects", prices="Prices", process="How we work", faq="FAQ", contact="Contact"),
    title=dict(home="HI Comfort demo site", services="Services · HI Comfort", projects="Projects · HI Comfort", prices="Prices · HI Comfort",
               process="How we work · HI Comfort", faq="FAQ · HI Comfort", contact="Contact · HI Comfort"),
    footer_l="HI Comfort · full renovations and finishing works · Varna", footer_r="Demo concept, not the company's official website",
    mbar=("Quick actions", "Call", "Viber", "Quote"), themes_aria="Colour scheme (demo only)", themes_label="Colour",
    rating="rating on Google ›", hero_eyebrow="Full renovations and finishing works · Varna",
    hero_h=("Your comfort,", "our renovation."),
    hero_lead="We take on the renovation of your home from the first site visit to the last skirting board. One team, one quote, one person responsible for everything.",
    cta_visit="Book a site visit", cta_calc="Estimate the price", tel_line=("Or call us:", "Mon–Sat"),
    plan_aria="Interactive apartment plan", plan_top="Plan · sample apartment",
    proof=(("5.0 ★", "read the Google reviews"), ("283", "followers on Facebook"), ("Mon–Sat", "open six days, book a visit")),
    home_srv=("Services", "Everything for your home.", "From one contractor."), all_services="All services",
    ba_head=("Before and after", "Grab the circle and slide.", "The difference speaks for itself."),
    ba_note="Illustration for the demo. Real before and after photos from HI Comfort's projects go here.",
    all_projects="See all projects",
    g_head=("What you get", "Promises on paper.", "Not just in words."),
    g=(("€", "A price written into the quote", "You know the amount before we start. It changes only if you ask for something extra."),
       ("1", "One point of contact", "No chasing tradesmen by phone. One person knows everything about your project."),
       ("◷", "A schedule with dates", "You see the stages in advance and when each one ends."),
       ("✓", "A clean handover", "We remove the waste and hand over the home ready to move in.")),
    g_note="Suggested wording. The owner confirms the terms before the site goes live.",
    rev=("Our clients rate us five stars on Google", "Read what people we have already renovated for say, and see more projects on Facebook.",
         "Google reviews", "Facebook page", "5 out of 5 stars"),
    band=("Ready for a site visit?", "We come to you, take measurements and give you a written quote.", "Book a site visit"),
    srv_head=("Services", "Everything for your home.", "From one contractor.", "Pick a single service or leave the whole renovation to us."),
    srv_main="MAIN SERVICE", srv_cta="Get a quote",
    srv=(("Full apartment renovation", "Demolition, wiring and plumbing, screeds, plastering, flooring, doors and paint. You talk to one person and we coordinate every trade."),
         ("Bathroom renovation", "Waterproofing, new plumbing and wiring, tiling and fitting the sanitaryware."),
         ("Kitchen", "Connections for the appliances, splashback and floor tiles, walls prepared for the units."),
         ("Flooring", "Laminate, porcelain tiles and parquet, with the subfloor prepared first."),
         ("Plastering and painting", "Smooth walls and ceilings, drywall, decorative plaster."),
         ("Windows and doors", "Advice on what to choose, fitting and finishing around the openings."),
         ("Wiring and plumbing", "New routes, fuse boards, sockets and lighting to plan.")),
    prj_head=("Projects", "Finished homes.", "Browse by room.", ""),
    filters=("All", "Bathrooms", "Kitchens", "Living rooms and bedrooms"),
    prj_note="The tiles show materials in place of photos. On the finished site each one opens a gallery from the real project.",
    lb_close="Close", lb_note="Space for photos from the real project.",
    cats=dict(bath="Bathroom", kitchen="Kitchen", living="Living room and bedroom"),
    items=(("Bathroom with large-format porcelain", "New plumbing and wiring, waterproofing, marble-effect slabs and brass details."),
           ("Living room with oak parquet", "Levelled subfloor, herringbone parquet, skirting and paint."),
           ("Kitchen with a tiled splashback", "Appliance connections moved, tiles on the splashback and floor."),
           ("Bathroom in dark stone", "Walk-in shower level with the floor, linear drain, concealed cistern."),
           ("Bedroom with decorative plaster", "Smooth walls, decorative plaster behind the bed, new lighting."),
           ("Kitchen with a terrazzo floor", "Terrazzo floor tiles, new wiring, suspended ceiling."),
           ("Living room with a feature wall", "Plastering, two-colour paint, laminate and interior doors."),
           ("Kitchen corner with brick", "Decorative brick, connections for an island and new flooring.")),
    prc_head=("Price estimate", "What will it cost?", "Work it out in 10 seconds.", ""),
    area_label="Size of the home", lvl_label="Type of renovation",
    lvl=(("Refresh", "Patch plastering, painting and small repairs."),
         ("Standard", "New wiring and plumbing, screeds, flooring, plastering and paint."),
         ("Turnkey", "A standard renovation plus bathrooms, doors, lighting and finishing, ready to move in.")),
    k_for="Estimate for", exact="Get an exact quote", prc_note="Example figures for the demo. HI Comfort sets the real prices.",
    offer="I'm interested in a {type} renovation of {area} m². Estimate: {price}.",
    prs_head=("How we work", "Five steps.", "No surprises along the way.", ""),
    steps=(("Site visit", "We come to you, measure and listen to what you want."), ("Quote", "You get a written quote listing the work, materials and timeline."),
           ("Contract", "We put the price, deadline and payment stages in writing."), ("Renovation", "We work to the schedule and show you the progress."),
           ("Handover", "We clean up and walk through every room with you.")),
    faq_head=("Common questions", "Before you call.", "Short answers.", ""),
    faq=(("How long does a renovation take?", "It depends on the size and the work involved. The deadline goes into the quote after the site visit, so you know the date in advance."),
         ("Can I live in the home during the renovation?", "With a partial renovation it is often possible. For a full renovation we recommend the home is empty. We discuss it at the site visit."),
         ("Do you buy the materials?", "We can handle the supply, or work with materials you choose. We help you pick flooring, tiles and windows."),
         ("How do I pay?", "In stages set out in the contract. You pay for completed work, not everything up front."),
         ("Do you work outside Varna?", "We work in Varna and the region. Call us and we'll tell you whether we cover your address.")),
    ct_head=("Contact", "Book a site visit.", "We reply the same day."),
    ct_rows=(("Phone and Viber", None), ("Email", None), ("Address", "25 Tsar Asen I St, Varna"), ("Opening hours", "Mon–Fri 8:00–18:00 · Sat 9:00–18:00")),
    ct_map="Open in Google Maps", form_h="Request a quote",
    f=("Name", "Phone", "Type of renovation", "Size (m²)", "What would you like us to do?", "Send request"),
    f_types=("Full renovation", "Bathroom", "Kitchen", "Flooring", "Plastering and paint", "Other"),
    form_missing="Please fill in your name and phone so we can get back to you.",
    form_demo="This is a demo and the request was not sent. On the finished site it goes straight to HI Comfort by email and Viber.",
    rooms=dict(
        hol=("Living room", "24 m²", ("Plastering and painting walls and ceiling", "Laminate or parquet with skirting", "Suspended ceiling with hidden lighting", "Interior doors")),
        kuhnya=("Kitchen", "12 m²", ("Wiring and plumbing points for every appliance", "Splashback and floor tiles", "Walls prepared for the units")),
        banya=("Bathroom", "5 m²", ("Waterproofing of floor and walls", "New plumbing and wiring", "Porcelain and wall tiles", "Sanitaryware and accessories fitted")),
        koridor=("Hallway", "6 m²", ("New fuse board and cable routes", "Hard-wearing flooring", "Finishing around the front door")),
        spalnya=("Bedroom", "16 m²", ("Levelled walls", "Flooring and skirting", "Paint in your chosen colour", "Door and lighting")),
        terasa=("Terrace", "8 m²", ("Enclosing and glazing", "Thermal insulation", "Flooring for outdoor conditions"))),
    # text swaps for the Bulgarian SVG pieces
    svg={"План на апартамент с шест помещения": "Apartment plan with six rooms", "11,40 m": "11.40 m", "8,40 m": "8.40 m",
         'aria-label="Хол"': 'aria-label="Living room"', ">Хол<": ">Living room<", 'aria-label="Кухня"': 'aria-label="Kitchen"', ">Кухня<": ">Kitchen<",
         'aria-label="Баня"': 'aria-label="Bathroom"', ">Баня<": ">Bathroom<", 'aria-label="Коридор"': 'aria-label="Hallway"', ">Коридор<": ">Hallway<",
         'aria-label="Спалня"': 'aria-label="Bedroom"', ">Спалня<": ">Bedroom<", 'aria-label="Тераса"': 'aria-label="Terrace"', ">Тераса<": ">Terrace<",
         "Баня след ремонт": "Bathroom after renovation", "Баня преди ремонт": "Bathroom before renovation",
         "Злато и графит": "Gold and graphite", "Среднощно синьо и шампанско": "Midnight and champagne", "Смарагд и месинг": "Emerald and brass",
         "Бордо и шампанско": "Bordeaux and champagne", "Еспресо и мед": "Espresso and copper", "Оникс и платина": "Onyx and platinum",
         ">Преди<": ">Before<", ">След<": ">After<", "Плъзгач преди и след": "Before and after slider"},
),
}

HEAD_JS = "(function(){try{var d=document.documentElement,t=localStorage.getItem('hc-theme');if(t)d.setAttribute('data-th',t);if(sessionStorage.getItem('hc-nav')){sessionStorage.removeItem('hc-nav');d.className+=' arrive'}}catch(e){}})();"
MATERIALS = [("bath", "m-marble"), ("living", "m-oak"), ("kitchen", "m-tile"), ("bath", "m-slate"),
             ("living", "m-plaster"), ("kitchen", "m-terrazzo"), ("living", "m-sage"), ("kitchen", "m-brick")]
LVL_RATES = [(110, 170), (260, 360), (430, 580)]
SCENE = dict(services="level", projects="tiles", prices="tape", process="steps", faq="plan")

LOGO, VLOGO, THEMES = read("logo.svg"), read("veil-logo.svg"), read("themes.html")


def swap(text, t):
    for a, b in t["svg"].items():
        text = text.replace(a, b)
    return text


def build(lang, page):
    t = T[lang]
    root = "" if lang == "bg" else "../"
    files = FILES[lang]
    href = lambda p: "./" if p == "home" else files[p]
    other = t["other"]
    other_file = FILES[other][page]
    if lang == "bg":
        other_href = "en/" + ("" if page == "home" else other_file)
    else:
        other_href = "../" + ("" if page == "home" else other_file)

    def link(p, text, cls="", extra=""):
        c = f' class="{cls}"' if cls else ""
        return f'<a{c} href="{href(p)}" data-nav="{t["nav"][p]}"{extra}>{text}</a>'

    def navlinks():
        out = []
        for p in PAGES[1:]:
            on = ' aria-current="page"' if p == page else ""
            out.append(link(p, t["nav"][p], "on" if p == page else "", on))
        return "".join(out)

    def scene(head, kind, tag="h1"):
        lead = f'\n        <p class="lead">{head[3]}</p>' if len(head) > 3 and head[3] else ""
        return f'''<div class="scene">
    <canvas class="tape" data-kind="{kind}" aria-hidden="true"></canvas>
    <div class="wrap">
      <div class="head">
        <p class="eyebrow">{head[0]}</p>
        <{tag}>{head[1]}<span class="thin">{head[2]}</span></{tag}>{lead}
      </div>
    </div>
  </div>'''

    def head(h):
        return f'''<div class="head">
      <p class="eyebrow">{h[0]}</p>
      <h2>{h[1]}<span class="thin">{h[2]}</span></h2>
    </div>'''

    def band():
        b = t["band"]
        return f'''<div class="cta-band">
    <div class="wrap">
      <div><h2>{b[0]}</h2><p>{b[1]}</p></div>
      <div class="acts">{link("contact", b[2], "btn brass")}<a class="btn ghost" href="tel:{PHONE_TEL}">{PHONE}</a></div>
    </div>
  </div>'''

    def guarantees():
        cards = "".join(f'<div class="g"><div class="ic">{i}</div><div><h3>{h}</h3><p>{p}</p></div></div>\n      ' for i, h, p in t["g"])
        return f'''<section class="pg">
    <div class="wrap">
      {head(t["g_head"])}
      <div class="two">
      {cards}</div>
      <p class="note">{t["g_note"]}</p>
    </div>
  </section>'''

    def before_after(more):
        m = f'<div class="more">{link("projects", t["all_projects"], "btn ghost")}</div>' if more else ""
        return f'''<section class="pg">
    <div class="wrap">
      {head(t["ba_head"])}
      {swap(read("ba.html"), t)}
      <p class="note">{t["ba_note"]}</p>
      {m}
    </div>
  </section>'''

    def service_cards(n):
        out = []
        for i, (h, p) in enumerate(t["srv"][:n]):
            if i == 0:
                cta = link("contact", t["srv_cta"], "btn small brass", ' style="justify-self:start;margin-top:6px"')
                out.append(f'<div class="card wide"><span class="no">01 · {t["srv_main"]}</span><h3>{h}</h3><p>{p}</p>{cta}</div>')
            else:
                out.append(f'<div class="card"><span class="no">0{i+1}</span><h3>{h}</h3><p>{p}</p></div>')
        return "\n        ".join(out)

    hc = dict(lang=lang, locale=t["locale"], dim=t["dim"])
    extra = ""

    if page == "home":
        hc["rooms"] = {k: dict(n=v[0], t=f"{v[0]} · {v[1]}", l=list(v[2])) for k, v in t["rooms"].items()}
        proof_href = [f'href="{MAPS}"', f'href="{FACEBOOK}"', f'href="{href("contact")}" data-nav="{t["nav"]["contact"]}"']
        proof = "\n      ".join(f'<a {h}><b>{b}</b><span>{s}<i>›</i></span></a>' for h, (b, s) in zip(proof_href, t["proof"]))
        r = t["rev"]
        main = f'''<section class="hero">
    <div class="wrap hero-grid">
      <div>
        <a class="rating" href="{MAPS}"><b>{t["proof"][0][0].split()[0]}</b><span class="stars" aria-hidden="true">★★★★★</span><span>{t["rating"]}</span></a>
        <p class="eyebrow">{t["hero_eyebrow"]}</p>
        <h1>{t["hero_h"][0]}<span class="thin">{t["hero_h"][1]}</span></h1>
        <p class="lead">{t["hero_lead"]}</p>
        <div class="cta">
          {link("contact", t["cta_visit"], "btn brass")}
          {link("prices", t["cta_calc"], "btn ghost")}
        </div>
        <p class="tel-line">{t["tel_line"][0]} <a href="tel:{PHONE_TEL}">{PHONE}</a> · {t["tel_line"][1]}</p>
      </div>
      <div class="plan" aria-label="{t["plan_aria"]}">
        <div class="plan-top"><span>{t["plan_top"]}</span><span>71 m²</span></div>
        {swap(read("plan.svg"), t)}
        <div class="chips" id="chips"></div>
        <div class="room-info" aria-live="polite"><h3 id="room-title"></h3><ul id="room-list"></ul></div>
      </div>
    </div>
  </section>

  <div class="proof">
    <div class="wrap">
      {proof}
    </div>
  </div>

  <section class="pg">
    <div class="wrap">
      {head(t["home_srv"])}
      <div class="grid3">
        {service_cards(4)}
      </div>
      <div class="more">{link("services", t["all_services"], "btn ghost")}</div>
    </div>
  </section>

  {before_after(True)}

  {guarantees()}

  <section class="pg" style="padding-top:0">
    <div class="wrap">
      <div class="rev">
        <div><div class="big">{t["proof"][0][0].split()[0]}</div><div class="stars" aria-label="{r[4]}">★★★★★</div></div>
        <div><h3>{r[0]}</h3><p style="color:var(--stone);margin-top:6px">{r[1]}</p></div>
        <div class="acts">
          <a class="btn small" href="{MAPS}">{r[2]}</a>
          <a class="btn small ghost" href="{FACEBOOK}">{r[3]}</a>
        </div>
      </div>
    </div>
  </section>

  {band()}'''

    elif page == "services":
        main = f'''{scene(t["srv_head"], SCENE[page])}
  <section class="pg">
    <div class="wrap">
      <div class="grid3">
        {service_cards(7)}
      </div>
    </div>
  </section>
  {guarantees()}
  {band()}'''

    elif page == "projects":
        hc["cats"] = t["cats"]
        hc["items"] = [dict(t=a, d=b, c=c, m=m) for (a, b), (c, m) in zip(t["items"], MATERIALS)]
        f = t["filters"]
        main = f'''{scene(t["prj_head"], SCENE[page])}
  <section class="pg alt">
    <div class="wrap">
      <div class="filters" id="filters">
        <button class="chip" data-f="all" aria-pressed="true">{f[0]}</button>
        <button class="chip" data-f="bath" aria-pressed="false">{f[1]}</button>
        <button class="chip" data-f="kitchen" aria-pressed="false">{f[2]}</button>
        <button class="chip" data-f="living" aria-pressed="false">{f[3]}</button>
      </div>
      <div class="gal" id="gal"></div>
      <p class="note">{t["prj_note"]}</p>
    </div>
  </section>
  {before_after(False)}
  {band()}'''
        extra = f'''<dialog id="lb" aria-labelledby="lb-title">
  <div class="lb-img" id="lb-img"></div>
  <div class="lb-body">
    <div class="row"><h3 id="lb-title"></h3><button class="btn small ghost" id="lb-close" type="button">{t["lb_close"]}</button></div>
    <p id="lb-text" style="color:var(--stone)"></p>
    <p class="note">{t["lb_note"]}</p>
  </div>
</dialog>
'''

    elif page == "prices":
        hc["offer"] = t["offer"]
        btns = "\n            ".join(
            f'<button type="button" data-min="{lo}" data-max="{hi}" data-desc="{d}" aria-pressed="{"true" if i == 1 else "false"}">{n}</button>'
            for i, ((n, d), (lo, hi)) in enumerate(zip(t["lvl"], LVL_RATES)))
        main = f'''{scene(t["prc_head"], SCENE[page])}
  <section class="pg">
    <div class="wrap">
      <div class="calc">
        <div class="in">
          <div>
            <label for="area">{t["area_label"]}</label>
            <div class="area-val"><span id="area-out">65</span> m²</div>
            <input type="range" id="area" min="20" max="160" step="1" value="65">
          </div>
          <div>
            <label id="lvl-label">{t["lvl_label"]}</label>
            <div class="seg" id="lvl" role="group" aria-labelledby="lvl-label">
            {btns}
            </div>
          </div>
        </div>
        <div class="out">
          <span class="k">{t["k_for"]} <span id="k-area">65</span> m²</span>
          <div class="price" id="price"></div>
          <p id="lvl-desc"></p>
          {link("contact", t["exact"], "btn brass", ' id="to-offer" style="justify-self:start"')}
          <p style="font-family:var(--mono);font-size:.7rem">{t["prc_note"]}</p>
        </div>
      </div>
    </div>
  </section>
  {guarantees()}
  {band()}'''

    elif page == "process":
        steps = "\n        ".join(f'<div class="step"><h3>{h}</h3><p>{p}</p></div>' for h, p in t["steps"])
        main = f'''{scene(t["prs_head"], SCENE[page])}
  <section class="pg">
    <div class="wrap">
      <div class="steps">
        {steps}
      </div>
    </div>
  </section>
  {guarantees()}
  {band()}'''

    elif page == "faq":
        qs = "\n      ".join(f'<details{" open" if i == 0 else ""}><summary>{q}</summary><p>{a}</p></details>' for i, (q, a) in enumerate(t["faq"]))
        main = f'''{scene(t["faq_head"], SCENE[page])}
  <section class="pg">
    <div class="wrap" style="max-width:860px">
      {qs}
    </div>
  </section>
  {band()}'''

    else:  # contact
        hc["formMissing"], hc["formDemo"] = t["form_missing"], t["form_demo"]
        c, rows, f = t["ct_head"], t["ct_rows"], t["f"]
        opts = "".join(f"<option>{o}</option>" for o in t["f_types"])
        main = f'''<section class="contact" id="kontakt">
    <canvas class="tape" aria-hidden="true"></canvas>
    <div class="wrap cgrid">
      <div class="info">
        <p class="eyebrow">{c[0]}</p>
        <h1>{c[1]}<span class="thin">{c[2]}</span></h1>
        <div class="row"><span class="k">{rows[0][0]}</span><span class="v"><a href="tel:{PHONE_TEL}">{PHONE}</a></span></div>
        <div class="row"><span class="k">{rows[1][0]}</span><span class="v"><a href="mailto:{EMAIL}">{EMAIL}</a></span></div>
        <div class="row"><span class="k">{rows[2][0]}</span><span class="v">{rows[2][1]}</span></div>
        <div class="row"><span class="k">{rows[3][0]}</span><span class="v">{rows[3][1]}</span></div>
        <a class="btn brass" style="justify-self:start" href="{MAPS}">{t["ct_map"]}</a>
      </div>
      <form id="form" novalidate>
        <h3>{t["form_h"]}</h3>
        <div class="f2">
          <div><label for="f-name">{f[0]}</label><input type="text" id="f-name" autocomplete="name" required></div>
          <div><label for="f-tel">{f[1]}</label><input type="tel" id="f-tel" autocomplete="tel" required></div>
        </div>
        <div class="f2">
          <div><label for="f-type">{f[2]}</label><select id="f-type">{opts}</select></div>
          <div><label for="f-area">{f[3]}</label><input type="number" id="f-area" min="1" inputmode="numeric"></div>
        </div>
        <div><label for="f-msg">{f[4]}</label><textarea id="f-msg"></textarea></div>
        <button class="btn brass" type="submit">{f[5]}</button>
        <div class="msg" id="form-msg" role="status"></div>
      </form>
    </div>
  </section>'''

    veil_label = t["slogan"] if page == "home" else t["nav"][page]
    alt_bg = "/" + ("" if page == "home" else FILES["bg"][page])
    alt_en = "/en/" + ("" if page == "home" else FILES["en"][page])
    m = t["mbar"]
    lang_link = f'<a class="lang" href="{other_href}" data-nav="{t["other_name"]}" lang="{other}" aria-label="{t["other_name"]}">{t["other_label"]}</a>'
    return f'''<!DOCTYPE html>
<html lang="{t["html_lang"]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>{t["title"][page]}</title>
<link rel="alternate" hreflang="bg" href="{alt_bg}">
<link rel="alternate" hreflang="en" href="{alt_en}">
<script>{HEAD_JS}</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Unbounded:wght@300;500;700&family=Golos+Text:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}assets/site.css">
</head>
<body>

<div class="veil boot" id="veil" aria-hidden="true">
  <div class="veil-in">
    {VLOGO}
    <div class="veil-name">HI COMFORT</div>
    <div class="veil-bar"><i></i></div>
    <div class="veil-sec" id="veil-sec">{veil_label}</div>
  </div>
</div>

<div class="ribbon">{t["ribbon"]}</div>

<header>
  <div class="wrap bar">
    <a class="logo" href="{href("home")}" data-nav="{t["nav"]["home"]}" aria-label="{t["logo_aria"]}">
      {LOGO}
      <span>HI COMFORT<small>{t["logo_sub"]}</small></span>
    </a>
    <nav class="main" aria-label="{t["menu_aria"]}">{navlinks()}</nav>
    <div class="right">
      {lang_link}
      <a class="btn small brass" href="tel:{PHONE_TEL}">{PHONE}</a>
      <button class="burger" id="burger" aria-label="{t["burger"]}" aria-expanded="false" aria-controls="drawer"><span></span></button>
    </div>
  </div>
  <div class="drawer" id="drawer">{link("home", t["nav"]["home"], "on" if page == "home" else "")}{navlinks()}</div>
</header>

<main>
  {main}
</main>

<footer><div class="wrap"><span>{t["footer_l"]}</span><span>{t["footer_r"]}</span></div></footer>

<div class="mbar" aria-label="{m[0]}">
  <a href="tel:{PHONE_TEL}">{m[1]}</a>
  <a href="viber://chat?number=%2B359898643973">{m[2]}</a>
  {link("contact", m[3], "p")}
</div>

<div class="themes" id="themes" role="group" aria-label="{t["themes_aria"]}">
  <span>{t["themes_label"]}</span>
{swap(THEMES, t)}
</div>

{extra}<script>window.HC={json.dumps(hc, ensure_ascii=False)};</script>
<script src="{root}assets/site.js"></script>
</body>
</html>
'''


def main():
    shutil.rmtree(OUT, ignore_errors=True)
    os.makedirs(os.path.join(OUT, "assets"))
    os.makedirs(os.path.join(OUT, "en"))
    for n in ("site.css", "site.js"):
        shutil.copy(os.path.join(SRC, n), os.path.join(OUT, "assets", n))
    for lang in ("bg", "en"):
        for page in PAGES:
            path = os.path.join(OUT, "" if lang == "bg" else "en", FILES[lang][page])
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(build(lang, page))
    print("built", 2 * len(PAGES), "pages into", OUT)


if __name__ == "__main__":
    main()
