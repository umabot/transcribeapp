# Transcription

## Metadata
- Created: 2025-01-15 14:43:31
- Source File: Robin setup Admin - 2025_01_10 15_37 CET - Recording.mp4
- File Size: 743.40 MB
- Duration: [Audio duration will be added in future version]
- Format: MP4
- Language: en-US
- Speakers: 3
- Diarization: Enabled

## System Information
- Operating System: Darwin (Darwin Kernel Version 24.2.0: Fri Dec  6 19:04:03 PST 2024; root:xnu-11215.61.5~2/RELEASE_ARM64_T8132)
- Python Version: 3.12.8
- AWS Region: eu-west-3

## Processing Information
- Transcription Service: AWS Transcribe
- Language: en-US
- Output Format: Markdown

## Content



**spk_0**: Here we are Fantastic So um left hand side are the main um Objects that you want to to manipulate So we want to start with assessments uh which assessment it's a handle so it's just an empty object And it's made of criteria So um an assessment it's a list of criteria because this is where we start We start with the criteria because this is what we want to evaluate when we are running a a role play Mhm OK Um then I will we will get into the details of the criteria uh in a second Then you've got the personas a persona basically it's a face and a voice Yeah uh is it No no no it's more than that sorry Persona it's uh it's also a background story So uh it's a it's a role it's a CEO it's a marketing director it's a sales first sales director you name it Yeah And it's made of an avatar and an avatar is a face and a voice Sorry for the confusion And finally you've got the scenario the scenario It's Picking a persona And we are describing a situation between The user and the persona and we also assigning multiple assessments one or many or well 0 to many assessments to evaluate this conversation and that's the overview of how you create a scenario

**spk_1**: Yeah Yeah

**spk_0**: Yeah good OK Uh users it's just to display the users of your board or tenant So and to the right

**spk_2**: yeah no they can create a new user as well So if you want someone to use the platform as a user you can create a hit You have to make sure that the flag admin is not check

**spk_1**: OK

**spk_0**: because they're not admin if they're admin they can access this UI If they're not they will not Uh the other thing the email at the moment we will fix that but at the moment make sure the email is unique I know it's not very easy but Uh it's unique across all the tenants all the orgs You you don't know so it maybe it should it should raise an error message I'm not sure But uh for instance you can see that I've got my if you look at my email address it's Guillaumehb.pro plus robin because you can do that in Gmail I don't know if you knew but if you had a plus next to RJ 28523 Yes you you can virtually create as many email addresses but they will all end up in your RJ 28523 inbox

**spk_1**: OK

**spk_0**: right so it's a trick by Gmail so you can create multiple email addresses

**spk_1**: Oh cool

**spk_0**: Well create you don't create them but it allows you to take yeah exactly Yeah OK so um In assessments if you go to assessments we can start preaching and so I treated an empty one So let let's take maybe we could use your um design thinking workshop what do you think just to to make it real So what what are you evaluating when someone is having a Uh a design thinking conversation maybe we need to figure out where in the double diamond the conversation is happening Right So maybe it's at the very beginning it's where we're trying to discuss with an end user and try to validate

**spk_1**: Yes empathy mapping for example yeah OK

**spk_0**: So it could be empathy mapping So you can so you give a name to the so the UI is not the best We are aware of it but we're not focusing on the UI of the admin interface yet We are we're focusing on So yeah at the top you've got the assessment's name so you can type empathy Mapping evaluation or assessment OK then in the description you give more information It's just a description it has no impact But just document what we want to do with this assessment OK And you save it So it's an empty thing it's just a group it's used as a handle to group criteria OK and I think you need to click on the icon not on the on the text

**spk_2**: You you have to click on the on the icon You will receive a safe message that was saved Now it's OK

**spk_0**: Yeah done And now you can add criteria underneath so you can click on add criteria Yep And you can edit it So you click on it new criteria

**spk_1**: yeah

**spk_0**: And here you can edit it Do you click on edit Yes yeah You're mute Oh OK it's coming back So you click on the criteria and here you can give it a name So uh what what are we evaluating specifically

**spk_1**: OK um so in the empty mapping we had like what is the see here and all those things what was it called called

**spk_0**: OK so um OK fantastic so We we want to evaluate that they asked what do you see

**spk_1**: Yes

**spk_0**: So the user asked the persona what they are seeing in their uh yeah OK yeah you can you can keep it like that You say you say what you let's let's be a bit more specific Let's specify it's about design thinking to help the AI a little bit

**spk_1**: Yeah OK So um

**spk_0**: So description it's the user asked the persona what they are seeing Yeah and then Hearing

**spk_1**: What was the other one trying to remember the design thinking uh feel

**spk_0**: feel is the feel here see say Yes and there's 4th 1 but yeah Anyway yeah it's just once again just an example So you can and then you are going to here you can guide the AI on how it's going to evaluate by giving it examples of You know this is what the user said or asked but OK you don't have to do it because Silvio has developed a nice Uh magic wand for you To help you draft to first version So if you save it first the steps are

**spk_2**: are you can go up and save yeah

**spk_0**: first you need to save It's counterintuitive at the moment but

**spk_2**: yeah we we don't focus on the user interface

**spk_0**: We don't and you click on generate guidelines See the magic wand You you click here

**spk_2**: Wait for a second a couple of seconds yeah that's it then go down

**spk_1**: Ah Uh oh OK Oh I I like it Very nice

**spk_0**: And then you can of course refine it because you know the more the more context you give the AI In the title and description the more I read this the score score guideline will be Yes Can I modify it Yeah absolutely and you can try again so you need to save again You you have to save you have to save first Oh

**spk_1**: oh sorry

**spk_2**: Yeah the water flow is not

**spk_0**: The US is fine

**spk_1**: Yeah that's fine I I you and I know worse workflows in this

**spk_0**: uh I think it I think I think it

**spk_2**: it reverted to the previous version yeah OK

**spk_1**: yeah yeah

**spk_0**: It has reverted to the previous version OK No but that oh no it has not OK no it's good thinking

**spk_1**: thinking There you go Yes yes yes

**spk_0**: so you can yeah you can treat multiple criteria as many as you want actually

**spk_1**: So you can say

**spk_2**: say say it again because it's not safe And

**spk_1**: it's actually suggested the title as well yeah

**spk_2**: yeah it suggests

**spk_1**: Oh so clever OK

**spk_0**: And then you can get back to the assessment and create if you want to but we don't need to for the for the demo Creat as many criteria as you want OK OK now let's go and create the persona we're going to um Yeah to to interview so you could create a new persona

**spk_1**: Yeah So first

**spk_0**: you must select the avatar Like I said the avatar is just a face and a voice

**spk_1**: Yes Be Remember we had a persona as well in design thinking

**spk_0**: Did we

**spk_1**: Yes the lady who went to Paris What was her name

**spk_0**: So you you're on mute

**spk_2**: You have to put the name of the persona

**spk_0**: You can put but yeah that that is the name of the avatar Yeah and then you need to give her name

**spk_1**: I think it was you now wasn't it

**spk_2**: I don't know

**spk_1**: I it been that long

**spk_0**: So you need to give her a title um You don't like that So attitude personality buy a role and traits to give the AI more meat when it will be role playing it Yeah

**spk_1**: go Yeah

**spk_0**: yeah exactly Yeah yeah when we will rewrite the the UX we definitely need to put some bubble helps here

**spk_1**: Yeah like uh I can't help or something

**spk_2**: Yeah exactly that's a yeah

**spk_1**: Is there such thing as a track called American

**spk_0**: You can do it And then you can give her a bio no she is uh so you remember about yeah she is uh 25 years old 30 years old consultant Living in New York blah blah blah She's single

**spk_2**: Too much information yeah

**spk_1**: Um

**spk_0**: Pro

**spk_2**: You have to go up and save OK before leaving

**spk_1**: OK All right I'll save OK

**spk_0**: And you know you know that it works in safari OK so we've got Una and now we're going to write the scenario So that's the interview between The user so and the persona

**spk_2**: The the scenario here is a thing I have to fix I'm looking at next to a scenario at the top If you click there you will see the field So this is a scenario name Put the scenario name there

**spk_1**: OK scenario uh taking interview

**spk_2**: Oh yes I'm editing everything that taking notes everything like this Quick OK

**spk_1**: Hm

**spk_0**: OK So the situation is basically the situation Between the between the interviewer and the interviewee is the first time they are meeting do they know each other you know things like that

**spk_2**: Yes You don't have to put una Oh OK You you can you can wait wait uh sorry you could

**spk_0**: could yeah

**spk_1**: you could you can you don't need

**spk_2**: need that because remember that then the user in the exercise they can change the name of you OK that it will

**spk_0**: will it will change anyways No no you can keep you can keep

**spk_2**: keep it OK that's a good experiment Let's see

**spk_1**: see what it does We can try yeah

**spk_0**: I'm confused by uh I'll let you finish Robin C I'm confused by the scenario type B2B

**spk_2**: This is to be a scenario

**spk_0**: It's um uh to be gone so it should be checked by default

**spk_2**: It's checked by the false by default so it's B2B scenario So if you want to change to B2C you have to save edit and then you check box B2C scenario

**spk_0**: OK

**spk_2**: so it's it's a B2BS scenario OK now

**spk_0**: OK so um yeah cold call is not bad We should create for you for instance uh an interview uh or um design thinking interview because in the cold call you will you will hear it's gonna be interesting but she's really cold call like she thinks that you are going to try to sell her something So maybe maybe put a uh a scheduled call the last one

**spk_1**: one OK

**spk_0**: So AI is role played by a user A buyer user is role playing a sales We've got silo if you look at the you I've got some uh MD markdown issue And their scenario mode Um and oh Silvio can you remove the AI difficulty also

**spk_2**: Uh

**spk_0**: can you select yeah yeah can you select medium because we're going to use medium medium

**spk_2**: I will select by medium yeah OK

**spk_0**: no no no yeah you hide it and by default it's going to be uh medium insert and here you won't select your persona John that's your yeah no that's weird That should not be John Look at that still you Why do we have John here Is the the public one

**spk_2**: Go go back to all the scenarios

**spk_0**: No let's say first for some reason I've got I've got an idea maybe it's because of the

**spk_2**: Yeah where they where they go down or go with the scenarios again go to scenarios

**spk_0**: Yeah uh

**spk_2**: Sean I don't know why OK let me check on this one I'm putting a note here OK I when I was doing that it was OK So you have to edit click on edit at the top

**spk_0**: Uh yes

**spk_2**: I did usually on the on the on the pencil click on the pencil

**spk_0**: pencil not on the text but on the on the icon yeah yes the icon yes

**spk_2**: I will change that also on the let me see notes Uh icons Save and they did

**spk_1**: Yup

**spk_2**: Improve your eye I re

**spk_1**: re scenario

**spk_2**: You have to say remember I that but it did the changes

**spk_1**: Yeah I tried the magic wand Yeah yeah OK I like the wording

**spk_0**: wording If you scroll down

**spk_2**: down and the persona But still John of course No go go and edit and change the persona for some reason it's not

**spk_0**: And it only rewrote the situation by the way yeah

**spk_2**: so select person's just it just uh OK let me see it's only shown for some reason

**spk_0**: It's the public one It's the only one with the public talent

**spk_2**: yeah because Uh But at the beginning was this is a B2C

**spk_0**: This one is a B2B

**spk_2**: Is a B2B or B2

**spk_0**: B2B But by default what is it you tell me

**spk_2**: No it's it's B2B by default But click on again Save it Let me see Not that we can continue with that but for some reason I don't know yeah change and then show me the scenario type B2B yeah it's OK Hm Wash what again OK continue I know I have to check why this happened No it's OK it's OK Mm Let me see on my and

**spk_0**: and and when when also Sylvia when Robin has clicked on the rewrite scenario he did not write the needs and the instructions and the objectives and You just remote the situation not the rest rest

**spk_2**: OK You should do it OK let me check on the LLM call because I'm using the wrapper for that Are you coming with the chase Yeah OK OK scenario one OK

**spk_0**: Robin sorry if that's a very bad demo Um

**spk_1**: no no it's that's fine It's a good test It's a good test

**spk_0**: And it's it's not a lot of people are seeing this interface so um So you will be interviewing John but let me you know what I'm going to do one thing for you Bear with me So you can use your persona I'm going to move your persona to public So everyone will see Una which is OK it's not secret And

**spk_1**: Uh John

**spk_0**: And now here you go OK so just save OK Maybe you need you need to refresh or try to try to edit Maybe it will refresh hopefully Scroll down try to see if you to see if you see Una In the sorry in the persona Ah OK No Edit No no no no no I've Una is still here but I moved her away somewhere else So if you go in the in the scenarios you should now be able to sign Una to your to your scenario OK You go to edit Senate tier Una yeah ah Great So context is um so the description it's really for you the admin The context will be will be for the um the the LLM the the the AI so Or you can say so the context is what is happening here or what happened before this call So the user is calling Una to understand her experience for for her travel in Paris or something like that

**spk_1**: yeah So uh so I would say the user is that right Mm Asking Who now on Uh Experience I think to Paris Would that be right OK OK

**spk_0**: And then she doesn't have any objections because it's not a sale Yeah OK And down you've got needs and habits This is where you also want to guide the AI because You know what are what what are her needs Well she likes to party let's say you know remember she she likes to party with friends she likes to visit uh museums blah blah blah Yeah What are her habits um she She likes touristic areas or she likes to discover new uh Find new things

**spk_1**: I know And meet people yeah

**spk_0**: and other info you could say uh she heard about She heard she she heard about I don't know something

**spk_1**: Mm Olympic

**spk_0**: yeah exactly

**spk_1**: Paris knew um

**spk_2**: Notre Dame OK that's good

**spk_0**: Yeah And these are the instructions for the user that will be displayed to the user So you are meeting with Una Yeah

**spk_1**: OK

**spk_0**: OK Um user referring is what they are trying to sell

**spk_1**: OK um airport Transportation To the hotel

**spk_0**: Yep And

**spk_1**: to us

**spk_0**: Hm And the objective yeah so and the objectives are um The objective of the call So you know it's really about asking what she heard what she saw what she you know remember

**spk_1**: To find out That she has heard to see And uh she Yeah About Travel Um traveling in Paris That right Yeah

**spk_2**: go up

**spk_0**: but just to to describe the options before you save So that if you scroll down user candidate company Um it allows the user to lead the company of the persona OK

**spk_1**: so she can be Amex or whatever she's

**spk_0**: she's from from No I'm talking about Una So uh you know potentially we said she works for uh uh what did we say she was working for She works for um

**spk_1**: in New York yeah

**spk_0**: so I think Deloitte yeah let's say she works for Deloitte

**spk_1**: Yeah but she can edit that

**spk_0**: potentially the the user can edit that yeah user cans offering they can edit what they are trying to sell and user can edit persona They can edit uh They can edit uh the persona title so the title so you know she's a consultant but she could be a CEO she could be something else

**spk_1**: Yeah

**spk_0**: OK And then so we need that

**spk_1**: yeah

**spk_0**: and you save And we

**spk_1**: we can say

**spk_0**: And yeah now you can just go to uh instead of going to admin.simplify you can open a new tab to chat.simplify Yep Yeah And if you go to practice You will have a private you should have hopefully Shoot I don't see it What's missing Hm Did we save it

**spk_2**: Yeah we say

**spk_0**: Can you go back to a I don't know

**spk_2**: I'm missing

**spk_0**: missing interesting OK try to add an assessment maybe that's the problem I don't think that's the problem

**spk_2**: problem Discover is scan yeah

**spk_1**: Oh but we we we I think we lost persona and assessment

**spk_2**: assessment assessment

**spk_0**: uh no assessment is still here

**spk_1**: That's the old one isn't it Where is the assessment Yes it it was the um Design thinking wasn't it

**spk_0**: Yeah let me let me check in the tables

**spk_2**: Are you with Robin

**spk_0**: No the the first one No one for

**spk_2**: for him when you created the tenant No

**spk_0**: what's what's that

**spk_1**: These are yours

**spk_0**: right Sylvia what's happening Yeah no OK we've got an issue here You should not see that That's OK

**spk_1**: Uh but there was one that we created yes because this is created by you

**spk_0**: and next steps You should not see that

**spk_2**: that Go back to the profile Click on profile Look at that It's public

**spk_0**: public now

**spk_2**: Yeah click on profile

**spk_1**: I should be living here right

**spk_0**: OK bear with me Uh let me let me check the yeah maybe it's the user When I changed Robin's user I just changed the tenant to your ID maybe not the the the tenant ID OK It's weird It should not happen We should fix that very quickly this standard to UAD thing

**spk_2**: thing yeah so like

**spk_1**: Uh

**spk_0**: sorry for that Robin At least at least at least you you see the mechanic then we've got some issues we need to fix because most of the time we are hard coding not hard coding but we we're doing everything by SQL Yeah

**spk_1**: And that's why why testing with me helps yeah because I I have no visibility on on on what's happening in the back end

**spk_0**: So talent ID I've got 199il you

**spk_2**: I have ah the problem is that There is only the tenant ID is the one that finished on B785

**spk_0**: Um Oh yeah I just changed the tenant ID not the tenant you you ID Bear with me because of that OK OK OK so uh let me Fix that on Robin's user

**spk_2**: Yeah I I got I don't I don't have rowing anymore on the growing something and that's it

**spk_0**: It's weird Um we need you to go back to your email log out It doesn't work yet you know that you need to open a private that OK can you get back to your uh email

**spk_1**: Yup start again again

**spk_0**: Yeah but you will need to open that into if you right click copy paste copy the URL or copy link Yeah copy link Now get back to Safario and you do file Private no you need to have a private um or if you do that in uh not in safari but in a In That's a small issue we need to fix also another one but

**spk_2**: No no cop copy paste the

**spk_0**: the link you Yeah OK Robin OK now we'll get back to assessments please OK cool OK And scenarios

**spk_2**: And also in persona should bea

**spk_0**: No Una she I moved her to Public maybe maybe I should maybe I should move it back to Robin's tenant and see what happens OK Bear with me

**spk_2**: Look it's there because

**spk_0**: because it's she's public now

**spk_2**: now Ah he's public OK yeah

**spk_0**: Um OK Let let first let let us make you test your scenario So open a new tab And you can go to chat.simplify Without the slash trial Yeah Go to practice And Shoot

**spk_2**: Oh because

**spk_0**: because what

**spk_2**: We have to check the because I think that uh when you check the 10 and your ID saving with the 10 and your ID of public yep yep yep OK oh it doesn't appear there Yeah it's there it's public interview on her experience in Paris OK

**spk_0**: OK let me that's OK let's say one thing It's super interesting OK thank thank that's that's thanks for being our guinea pig Robin You just uh found found a couple of things we need to fix not not big things but we need to to tweak them

**spk_1**: Uh that's right

**spk_0**: So that is correct but yeah so bear with me I'm going to fix that in a second and then it will appear as private uh scenario Yeah yeah

**spk_2**: If you change again to the tenant new idea of rowing Johnson Tenant yeah exactly this is what I'm going to do It's going to fix that and also the only thing that has to do is has to refresh

**spk_0**: Yeah if you refresh Yeah yeah that's private

**spk_2**: private That's yeah Yeah when when we changed up behind the scenes you then a new ID we put you in the public and you are saying everything in public That was fine

**spk_1**: fine Yeah that's OK Yeah

**spk_0**: So you want to try yeah you can try whatever you want OK Oh English We've got did you did you did we share the new voice the new American voice with you Well you will that's oh no no No sorry we have not deployed it yet so it's still the old one

**spk_1**: All right So it's English American or English British Yeah

**spk_0**: it's English American so far but we can change that at the tenant level so it could be English or OC if you want

**spk_1**: Oh OK nice That would be great But it um Uh what do you call it Airport transport You do work for

**spk_0**: OK

**spk_1**: She's um she's uh CXO What was she um lawyer wasn't she

**spk_0**: Maybe yeah she could be a lawyer

**spk_1**: Yeah Call it AX OK Uber Uber

**spk_0**: And the the the behavior might be a bit weird because it's going to be considered as a sales call Not an interview so

**spk_1**: Yeah Yeah and you you kind of use design thinking as a way of doing that anyway It's Uber

**spk_2**: I think it's a yesSubber.com Amex We have 2 websites of the company

**spk_1**: American Express.com

**spk_2**: Oh OK yeah

**spk_1**: Is that right Yep Mm Can you hear I I don't know if you can actually hear

**spk_0**: Uh we won't be able to hear it but it's OK

**spk_1**: OK we just OK Hello Una how are you Hello how are you

**spk_0**: I think it didn't get anything did it

**spk_1**: Uh hello Una how are you Hello Hua how are you

**spk_0**: And she's Emily by the way

**spk_1**: OK Hello Emily Uh I'm Robin Nice to talk to

**spk_0**: to you And look at the view she was first time visiting London

**spk_1**: I understand that you're making plans to travel to Paris Is that correct OK so she thinks that's going to London

**spk_2**: because she's going to London

**spk_0**: Sorry If you look at the personal details now she's going to she's going to London not Paris

**spk_1**: Ah OK

**spk_0**: All right we we asked the the the big we asked the AI to change the scenario but if you uncheck the 3 boxes if you uncheck the 3 boxes at the bottom of your scenario it will stay at this So she will be still Una and she will still be traveling to Paris

**spk_1**: OK Yeah

**spk_0**: So you want to check

**spk_2**: uh this one up and I did

**spk_1**: So do do I change it or

**spk_0**: or as you wish I yeah it might need some more tweaking now I'm thinking out loud here because the uh anyways so

**spk_1**: OK

**spk_0**: There's another thing can can you can can Robin edit his profile or not No not yet OK sure Because at your profile you can set what you are selling and who you work for So it can automatically be filled

**spk_1**: OK good because that'll be useful

**spk_0**: Well you try to try to uncheck user candidate company offering and persona But then you need to scroll up and say and edit the company yeah here company and company URL so she works for uh American Express Amex It was offering to to complete yeah

**spk_2**: Uh Gula sorry for that And also rowing Yeah if you go through profile you cannot change the profile there but if you go to users you will see your user rolling and you can edit your user And in the in the user you can edit the company that you're working which is your user offering which is your company and everything OK that's good That's good But you have to go through users and profile is only now read only OK I'm adding that as a feature OK but you can edit your profile that

**spk_1**: OK It

**spk_0**: And you can also select your language by default So by default it's English but you can say and we will add the the Asian languages Yeah And how how do you how do you how do you save Sylvia how do you save

**spk_2**: Uh click that Click there yeah

**spk_0**: OK

**spk_2**: it's safe OK OK so I have to wait OK use a language Add more languages and an enhancement And then

**spk_0**: Yeah

**spk_2**: doesn't change the the yeah

**spk_0**: the word is still edit and you can also edit your company weirdly enough it's here

**spk_2**: here but um

**spk_0**: company is at two places It's weird

**spk_1**: This is URL

**spk_0**: Yeah yeah but still you

**spk_2**: you give me a second just

**spk_0**: yes sorry Here you've got company known and if you scroll down I never went to this place you've got another company field which one is the correct one

**spk_2**: The company of the field Uh Yeah Yeah yeah it's none You're gonna you're gonna change that OK so for some reason uh OK that's a a back Let me check this user

**spk_0**: Don't spend too much time on that that it's OK

**spk_2**: No it's OK but it's easy Just a top company name OK

**spk_0**: let's see if you go back did you and check all the boxes Robin Yes yeah so if you go back to your scenario So uh you go on simplify if you click on the You need to rate give us give us a number of stars And practice again and now you should not have this intermediate You know the select Oh sorry it will work in the next it will work in the next release OK which is not deployed yet Ah OK yeah so she will still travel potentially to another place at the moment

**spk_1**: Is she still going to London

**spk_0**: No that changed She freaking to travel so you can ask her Yeah

**spk_1**: OK Hi Emily this is Robert here How are you Oh I'm curious to know what's your travel plans to Paris Uh do do you know anything about Paris Is this your first time to Paris So what are your expectations What are things you you like to see and what you hear about Paris at the latest Um How do you feel about using Uber um from the airport to your hotel

**spk_0**: Robin before you you move on we have not attached the evaluation yet So what it's going to do it's going to evaluate with a very um a very generic evaluation criteria

**spk_1**: OK

**spk_0**: So the the summary is very basic So now you can we didn't we didn't do that So if you get back to your scenario you can attach to the scenario one or multiple assessments To the right sorry no no no to the right Oh Yeah yeah you you'll need And then here are all the assessments you've got access to so that's the public ones That's the one you've created

**spk_2**: So you can you can save changes at the bottom Here is a on the sun

**spk_1**: Oh OK

**spk_0**: OK and now if you start again your simulation it's going to evaluate on so what yeah you can you've got to try again button try again not too late

**spk_1**: late Oh sorry

**spk_0**: That's all right

**spk_1**: It's pretty cool so far by the way

**spk_0**: Thank you Well except for the small bugs

**spk_1**: but yeah No no that's it's one of those things uh you you should discover along the way which is which is good right

**spk_0**: Honestly we don't we don't use the admin interface very often ourselves you know we don't create uh new stuff daily so it's cool to have this uh this month with you No she's Maria

**spk_1**: OK Maria hopefully going to Paris The name changes It is good Hello Maria how are you This is Robin here from Uber Hello this is Robin from Uber I understand that this is your first time in Paris What are some of your expectations of things that you like to do in Paris Have you used Uber in other countries before And how did you hear about Uber in Paris What's your thoughts on that That's pretty good isn't it OK Do do do OK All right That's pretty good isn't it Are you guys still there

**spk_2**: No you're a mute yeah

**spk_0**: as I said it's it's we tweaked a sales uh mode into a design thinking mode So we could create a new mode which is a design thinking mode to let the AI know you're not even trying to sell it anything

**spk_1**: Yeah Um yeah I I guess I suppose so but ultimately side thinking is really about selling But really this is a part of discovery almost isn't it And what I like it is that um you get to to to ask questions and things like that And and those questions are based on what you see here and everything around the uh around the uh empathy mapping So so it's a way good way of practicing your empathy mapping uh and probably next step would be how you define the solution what the problem is and I think that's that's probably like another stage you could put into here as a next scenario is you know what what are the potential issues that you have with with Uber for example what kind of things that you want to do what kind of problems do you have What jobs need to be done right So yeah I I you know within what an hour's time we we almost like did an exercise already um for your mapping design thinking

**spk_0**: Yeah yeah yeah I do see a couple of gaps because the name Una stayed in the instructions which makes sense because we don't touch the instructions We don't transform the instructions on purpose So uh yeah it's just a couple of things that the admin needs to be aware of

**spk_1**: OK instead of um the naming to Maria or Emily and some

**spk_0**: some some of the fields when you define a scenario some of the fields are not touched by the AI So it can create some discrepancy because like the instructions it's not touched by the AI It's not transforming It's not changing anything in the instructions So if you've got the name of the persona in the instruction and the AI decides to change the name of the the persona which is the the behavior by default yeah yeah then the instructions and persona name might Have some discrepancies so you don't want to to put the person name in the instructions for instance

**spk_1**: But would you say una is a name that's really for internal use as opposed to the actual person you're talking to

**spk_2**: in the scenario so probably because you are our first admin user OK on this one So the way that we design this is that as Guillo was explaining to you You start thinking what is the exercise that you want to to run with your you know clients or students or salespeople or design thinking people consultants and then in that scenario like this one you say well I want to to set up one scenario to evaluate how they are good on discovery and evaluate the empathy and doing that OK so so you put that into a scenario Then you have to assess that scenario and you will have different criteria So the criteria so you can have one criteria like in this one you can have more So think about like OK lines of analysis of the scenario OK on the assessment And then you put the persona but always we were doing that thinking about how to scale to personalize the coaching because if you put Una and everybody works with Una and Una only works for American Express everybody has Una working for American Express did OK You can ask people to do exercise on the ground and every time that that rerun the exercise the persona will be OK so My my question to you is how do you feel about that Because we are thinking about two things that every person that is on the coaching class let's say Yeah they will work on their own scenario All the scenarios for you as a coach OK on that class It's based on let's say a canonical scenario OK but everybody can adjust the details who they are talking to what they are selling to which company they are working for and everything And every time that they rerun the scenario these few things they will they will be tweaked as Guillain was saying So so how how do you feel that this is something So we think but do you think that this is powerful is useful in a coaching a scenario or

**spk_1**: Yes um the question is if you got say a scenario uh and you got here Una can you have one scenario but you can pick from a different number of role players or persona So let's say we're doing an interview but then we've got Una which is one avatar but uh Una could be the lawyer but it could be uh another interview but it will be a um I don't know Um another person that you you want to also ask but has a different um persona This is

**spk_2**: is why you go to go to personas and you can define as many personas that you need The personas are the characters that you will scenario Uh-huh In this moment every scenario only can have one person

**spk_1**: OK yeah so then when

**spk_2**: when you are talking you are talking the user is talking to only one Asian

**spk_1**: OK So if I need to have another persona I just create another another scenario No no

**spk_2**: you don't have to create You create a persona OK and then you have two options You can go to the same scenario and you can change the persona So for example if you want to so there are two scenarios here for you that we were seeing It's good that you test that You can have this scenario and you can have a persona that is una that you define and the trait of una for example you put that una is very friendly Yeah but then you can create another persona let's say Silvio and you say Silvio on the personality uh is a horrible introvert We'll never answer any question So then what you can do is you you can play with that You can have the same scenario and then in one class you change the persona and you are working with the OK with Una that is friendly or you are working with Silvio That is introact OK because you change the persona on the scenario That's one way to use that The other way is that you have different scenarios with different personas but you have to think when you are creating the class how is the relay So there are many ways which is why we're thinking about difficulties how we are putting everything into medium because we are tweaking that But one way that you can model how the persona is going to behave in this scenario is that you change the persona you add more personas you change the context uh whatever But then you use the same scenario The only thing that you do is you change the the persona assigned to the scenario

**spk_1**: Correct yeah So I can have multiple persona Yeah so I I've put

**spk_0**: put back I've puta back to your tenant so she belongs to you

**spk_1**: So now I can add Silvio and then what I do is I go to scenario and now I would then say instead of interview with Una you'll be interviewed with Silvio and Then I would just add in here Silvio for example once you

**spk_0**: yeah exactly

**spk_2**: exactly one some things that we have to to to change or to make better on the user interface for that mean as you know is that you go to a scenario interview with Una as you can say we we don't touch the name of the scenario when the agent is right OK so if you put Una in that place they will appear on the user scenario and maybe you don't want that OK so here is the interview with a person About that experience OK about traveling experience OK about what so Remember the scenario you have to think what you put here on the scenario That is a canonical scenario OK uh the same as a persona It's a it's a canonical persona It's a persona that is extrovert has a lot of experience has less experience uh shows I know it's angry it's always happy so so so you find canonical personas because why Because when when user run the the the the exercise The AI our model behind the scenes is going to tweak these things and it's going to create in that moment a character based on that persona and it's going to create a particular scenario based on what you put into the scenario This is why it's not good to put in the instructions You are talking to Una because this is going to be into the into the Asian they saying OK

**spk_1**: so Correct So so it should be just a general user but I can actually tweak the scenario um according to the exercise Yeah Yeah or I create another scenario with a different user for example You could so another situation where you've got the user is happy traveler or user is fussy traveler or or um so you can create different scenarios for different types of user personas Exactly Oh love it

**spk_2**: This is something we don't have you're our first Second big tester 2

**spk_0**: 2nd 2nd 2nd big tester Julia did a lot of tests

**spk_2**: Ah Julia did a lot of tests yes yeah yeah very nice So yeah

**spk_0**: hope hope you the the the the Yanmin interface how how do you find the interface

**spk_1**: Robin it's great It's fine O compared to Salesforce interface it's easy OK Take take the take the flowers

**spk_0**: flowers Sylvio the flowers Take the

**spk_1**: the flowers take the flowers Um what's interesting um just on this experience as you might have known Guilla when when we did the design thinkinging exercise you only had one persona In this case you can have multiple persona right So another this is now enhances the experience of uh of teaching Because remember if you recall when we did the design thinking you only had one Una right So yeah

**spk_0**: exactly That's that's exactly what what's that's one of the reasons we've got you know you can change una dynamically even the user can say Una she's actually not a lawyer she is uh an artist

**spk_1**: Yeah yeah you can change the scenario quite easily um based on on the the people you're training that you want to practice on which is quite important right Because um it's the context of that user that you want to interact with Yeah Question with the avatar Um can I select an avatar image or this is an AI generated

**spk_0**: but it's an AI generated generated We generated them If you need a specific type of characters just let me know more Asians I can do more Asians We've got one Asian male at the moment but if you need more Asian let me know or specific ethnicity or age or you know tell me what what you need and I will create more

**spk_1**: OK yeah just a variety you can select from Yeah

**spk_0**: at the moment we've got about 8 or 10 or 10

**spk_2**: But these are the so we created there 8 or 10 avatars OK from there you can see them OK we can create more train

**spk_0**: train is definitely 3 is uh engine Yeah uh when train is Asian Ah nice um and La Lu is uh no he's Very very very mature man yeah Rob Yeah we've got 5 yeah 5 and 5 Rob is a young white Edward is black

**spk_2**: Oh what memory I don't remember them

**spk_0**: Susan I don't

**spk_2**: don't

**spk_0**: I don't yeah it's just was just uh Susan is your favorite Silvio Yeah Rosa is a bit similar to to Susan to Susan So Tricia is black That is older that is older yeah I don't have a I don't have a yeah

**spk_1**: young Asian

**spk_0**: Asian young Asian yeah I should I can add a young Asian girl yeah I will

**spk_1**: Yeah OK nice I like it

**spk_2**: And and the avatars again as uh Guillaume said it's only An image and a voice OK that you attached to the persona to to give some visualization when you're running the scenario but really in really with one avatar you can have I know 1 10 100 1000 different personas always on the same avatar And then for each persona you change the personality the value and everything that you're going to use

**spk_1**: OK Now can I we were

**spk_2**: we were doing that based on our experience from from Salesforce and also my experience on Pega you know when when when you are designing the workshops and and a lot of work goes into defining which are the personas the characters that we are going to have here and we are going to do that which is a scenario which is a company and then you have to write the company scenario and everything's OK well yeah let's do that but also we say why we don't improve that when the user ran the the scenario The scenario can tweak based on the inputs on the first screen and this is what is happening

**spk_0**: Robin you had a question

**spk_1**: Yes I um so if if I I have a persona now I've created I can back go back and modify Yes So um

**spk_0**: OK And it will for the new when someone is going to use your scenario again it will change the it will change the behavior But you can say you know she's rude

**spk_1**: Yes

**spk_0**: instead of being open and friendly she's not rude but she's very closed and

**spk_1**: Yes quiet and yeah please let us know give us your feedback if

**spk_0**: that really works well because We we tried gosh we've worked a lot on the The prompt behind the scene hopefully it should take that into account

**spk_1**: OK Yeah I I'll I'll I'll definitely play with it And um uh and and that I guess this is where a lot of things that I can add value is when I speak to the customer potential customers I cannot say you know what are your typical customers What what kind of people you interact with so that when we do the exercise Size it simulates as if they are really talking to their customers or their business partner when they do B2B you know so so they can be it can be as most realistic it can be and that's where I can try to tweak that for them Yep Yeah that's my value add if you will because obviously you don't have time to do all of this um but that is where we can charge the extra customization um fee to to really sort of tune it to what they really the environment closest that that they are considering

**spk_2**: I I think it's a great point because one thing that I was experienced myself is when I'm testing and creating a scenario and persona I have no idea OK so usually I put OK very very vague things But when we are testing we figured out that the Asian improves on the on the reaction As much detail as you put in in in this in this attribute in the persona and the scenario but again that the and I think that you you hit a very good point when you are talking with the B2B customer You you know a company like Salesforce they find this type of people but then I can't say working for Musoft or Slack they will find they will interact with different type of people OK So and and this is what they would need help to to to customize the personas customize the scenarios customers the assessment as well OK the criteria of the assessment How do you want to

**spk_1**: to Indeed Very much

**spk_0**: one last one last thing you must be aware of um you are automatically disconnected after one hour whether you're moving doing something after one hour you clicked on the link Yeah you click on the link you have to log in again OK we're we're going to change that but yeah

**spk_1**: do I lose everything or do I still keep it

**spk_0**: if you did not save it you you will lose it yeah

**spk_1**: OK so but this assessment

**spk_0**: That's saved That is saved Yeah it's saved It's uh it's just you say you're creating a new scenario and you're forgetting to click on save If you're locked out you you lost it

**spk_1**: OK now if I had to log in

**spk_0**: no so logout doesn't work We've got an issue with logout We're going to change the the architecture

**spk_1**: architecture

**spk_0**: yeah we we will change the I know

**spk_1**: yeah oh yeah

**spk_2**: well it works in the sense that uh it destroyed the cookie somehow and

**spk_0**: oh gosh Uh so how do you log in again You want to go to you go on simplify and Yeah just click on login There is a login button it should work Yeah log in Uh Uh see no so no no you should you should have had The login the login page but it doesn't work Basically the logout does not work and you logged out after one hour

**spk_1**: Yeah Yeah So if I need to go back and and do this again uh where where do I go again

**spk_2**: Usually my my best practice do not confuse that uh rowing when I'm what I'm doing is I open a new incognito window in Chrome so I go to file go to file In the menu to see new incognito window So I always start with the new Incognito window because that will force the the login So I close incognito window So when I want to log out really log out I close the window I open a new window and start again That that will clean everything

**spk_1**: OK OK And now I need to do the same thing going by email So doing it incognito will allow me to to do that again

**spk_2**: Yeah yeah you have to go back to the incognito window now So so you have to copy the you have to copy the the the the the link there Um no no no no no go back to your email Copy in the line now copy the link Copy link Now go to incognate the window No yeah you can put that Yeah that's the thing Go put that

**spk_1**: There you go

**spk_0**: Oh yeah got it And now you the clock is ticking You've got one hour So what what what I'm doing usually I've got a timer here just to remind me oh OK I'm going to be logged out in 5 minutes OK

**spk_1**: fair enough We'll we'll fix

**spk_0**: fix that Silvio is going to work on that next week

**spk_1**: week OK all good all good Wonderful Uh yes

**spk_2**: but you know the um my role is not to push changes to production on a Friday night

**spk_0**: I know but I'm talking about odd odd

**spk_2**: uh no no no that OK are the things that give more flexibility OK let me let me finish the recording yeah yeah

**spk_1**: yeah thank you I've got I've got a call

---
Generated by AWS Transcribe Application
