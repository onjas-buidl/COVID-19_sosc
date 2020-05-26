# Housekeeping 

* need to put JHU data folder in the root folder 



## Evaluating Governmence by Country

* data issues 
  * owid-covid-data.csv  is from https://github.com/owid/covid-19-data/tree/master/public/data 
  * JHU data 

### What question to ask?

* influence of type of government on controlling the virus 
  * type of gov -- virus 
* explore a three-layer model: type of gov --affect--> direction/execution of policy --affect--> virus transmission
  * get to know the coefficients -- how gov affect policy, how policy affect virus 
  * hierarchical linear model? Just add another variable?
  * ML modelling? 
* Or answer the question: is the form of government a good determinant?
  * Alternatives: state-society relation -- any quantification work available?
  * culture score
    * https://www.hofstede-insights.com/product/compare-countries/
    * https://geerthofstede.com/research-and-vsm/
    * power distance, individualism, masculinity, uncertainty avoidance, long term orientation, indulgence
    * 

### Technical Issues

* choose proper variable to quanitfy virus severeity 
  * Virus severity 
    * avg. growth rate (current)
  * Policy**
    * pace of action -- time interval between first occurance and total lockdown (control)

### Other 

* potential research mentor 
  * Prof. Christopher Berry, Assoc. Prof. Anthony Fowler (field relevant!)
    * [UChicago news article](https://news.uchicago.edu/story/covid-19-pandemic-inspires-scholars-change-course?utm_source=newsletter&utm_medium=email&utm_campaign=UChicago_News_M05_07_2020&mkt_tok=eyJpIjoiTW1NME1USmxZakl4TmpoaCIsInQiOiJMZmtnTnlFWlczN2NwMUJsT011WXozXC9pc0tjWlJ3c3ZOcjhOeERnVzI1YzN1cGNcL21DY2tsK1V0Y3ZFcERydU9PTlJEWlVhR09sZE0xQnBlVlpCeEwxNUZHNUZXSE5GRjlyOVpXeUdTTlNRajl6S1pHQVdpVTJmaDBXRndsVFoyIn0%3D)
    * (a US version of measuring governmental response )
  * Dali Yang & Regina?
  * NYU Shanghai -- Christina Jenq 
* Peter Meeting 1
  * log regression -- growth rate 
  * maybe try exclusion criteria for days to calculate growth rate (num of days between 10 - 1000)
  * Diff-in-diff (utilize panel data) 

Dali Yang update!



# Prof Jenq May 22

May 22
* underreporting / measurement error
* effect is in terms of counterfactual -- measure effect in terms of that 
  * Book: (undergrad) Mastering metrics: the path from cause to effect, Josh Angrist, et al 
  * (grad) mostly harmless econometrics   
* find a research design to approximate the experiment to get the causal effect 
  * treatment: 'democracy'
  * control should account for the confouding factors: those affecting virus except democracy 
  * natrual experiment appraoch 
  * diff-n-diff: similar countries that differ in democracy 
  * other treatment variable: public health? Taiwan/S. Korea vs. US UK 
UCLA ''
https://stats.idre.ucla.edu/stata/seminars/stata-survival/ 

Synthetic control 
* whether counterfactual 
* history of that counterfactual -- look at history 
* matching based on important characteristics of the country -- use other control variables 
* ability to enforce lockdown (might ) 
  * Taiwan? no lockdown but did well 
  * Japan
* cultural score 

dependent variable 
* effectiveness: change in line 
* manually construct: smoothing, limit it to countries with more data 
* messy data: don't have 
* develop an algorithm how to select data 
* number of death, num of confirmed cases 

literature review 
* mass media articles -- collective/individualistic articles 
* political science literature: how effective government reacts 