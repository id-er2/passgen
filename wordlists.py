"""Small, hand-selected lists of ordinary words. No downloads at runtime."""

ENGLISH = tuple("""
apple apricot avocado banana berry cherry coconut date fig grape lemon lime
mango melon olive orange peach pear plum raisin almond hazelnut peanut walnut
barley bread butter cheese flour honey lentil noodle oat pepper potato pumpkin
radish rice salad sesame soup spinach squash tomato turnip wheat yogurt carrot
acorn bamboo branch cedar clover daisy fern flower forest garden grass leaf
maple meadow moss oak orchard palm petal pine pollen reed root rose seed
sprout stem thorn tree tulip vine willow wood beach brook canyon cave cliff
cloud coast creek desert dew dune earth field frost hill island lake mist
moon mountain ocean pebble pond rain rainbow river rock sand shadow shore
sky snow spring star stone stream summer sun thunder valley waterfall wave
wind winter basket blanket bottle bowl box brush bucket button candle carpet
chair clock cloth coat cotton cup curtain desk door drawer drum feather flag
flute fork glass glove hammer handle hat jacket jar kettle key ladder lamp
lantern lid mirror needle notebook paddle paper pencil pillow plate pocket pot
ribbon ring rope ruler scarf shelf shirt shoe shovel soap sock spoon table
thread towel tray umbrella vase wheel window wool boat bridge cabin castle
fence gate harbor house hut path porch road roof sail school tent tower
""".split())

ARABIC = tuple("""
تفاح مشمش موز توت كرز تين عنب ليمون مانجو شمام زيتون برتقال خوخ كمثرى
برقوق زبيب لوز بندق فستق جوز شعير خبز زبدة جبن دقيق عسل عدس معكرونة
شوفان فلفل بطاطس قرع فجل أرز سلطة سمسم حساء سبانخ طماطم لفت قمح لبن
جزر خيار بصل ثوم نعناع بقدونس زعتر قرفة زنجبيل كمون هيل زعفران خس
فاصوليا بازلاء باذنجان رمان بطيخ فراولة أناناس تمر جوافة كيوي زهرة شجرة
غابة حديقة عشب ورقة غصن جذع جذر بذرة وردة نخلة صنوبر بلوط صفصاف
خيزران سرخس طحلب حقل مرج بستان بتلة لحاء شاطئ نهر بحيرة بحر محيط
جبل تل وادي كهف صخرة حجر رمل حصاة سحابة مطر ثلج ضباب ندى صقيع
شمس قمر نجمة سماء ريح برق رعد موجة جزيرة خليج ساحل ينبوع شلال
كثيب ظل ربيع صيف خريف شتاء سلة بطانية زجاجة وعاء صندوق فرشاة دلو
زر شمعة سجادة كرسي ساعة قماش معطف قطن كوب ستارة مكتب باب درج
ريشة راية مزمار شوكة كأس قفاز مطرقة مقبض قبعة سترة جرة غلاية مفتاح
سلم مصباح فانوس غطاء مرآة إبرة دفتر مجداف ورق قلم وسادة صحن جيب
قدر شريط خاتم حبل مسطرة وشاح رف قميص حذاء مجرفة صابون جورب ملعقة
طاولة خيط منشفة صينية مظلة مزهرية عجلة نافذة صوف قارب جسر كوخ قلعة
سياج بوابة ميناء منزل خيمة برج طريق سقف شراع مدرسة فناء مقعد أريكة
""".split())

WORDLISTS = {"en": ENGLISH, "ar": ARABIC}
