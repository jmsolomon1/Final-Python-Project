# Great Recession Education Analysis Write Up:

“You will then spend *no more than 2-3 pages* writing up
your project.  You should describe your research question, then
discuss the approach you took and the coding involved, including
discussing any weaknesses or difficulties encountered.  Finish with a
brief discussion of results, and how this could be fleshed out in
future research.  The primary purpose of this writeup is to inform me
of what I am reading before I look at your code.”  

# Research Question:

    My research question involved looking at how the Great Recession (the
financial crisis that occurred from roughly December 2007 to June
2009) may have impacted science test scores for middle school students
in the United States.  I hypothesized that the period of economic
distress and elevated unemployment would have negatively impacted test
scores as families that suffer financial shocks are often less able to
provide for their children’s educational needs and that this would
have shown itself in diminished test scores.  I looked at data
involving US unemployment (and employment), free lunch participation,
national science test scores for 8th grade students and two articles
published shortly after the Great Recession that referenced how
parents losing their jobs negatively impacts their children in school.
I wanted to isolate the data for the years between 2007 and 2015
because that would show me what the levels were immediately before,
during, and after the Great Recession for each of those variables.
However, science testing was not consistent and I was only able to
secure data for the years of 2009, 2011 and 2015 so those are the
years I focused on.  While it was clear that unemployment sky-rocketed
during the Great Recession, it did not appear to have any influence on
national science test scores which appeared to slowly rise each year.
This was peculiar given that free lunch participation drastically
increased in the years after the Great Recession but my analysis was
unable to correlate any of these variables.  I was unable to prove
that the unemployment and financial distress caused by the Great
Recession negatively impacted science test scores for US students. 

    I have a few takeaways from the analysis, as well as comments on the
process of using Python to explore this topic.  I think it’s likely
that the science test scores are ‘less than accurate’ and that because
of the pressure to show students are doing well that the test scores
may not be an honest assessment.  If unemployment went up and free
lunch participation went up, it doesn’t make sense that students would
keep performing at or above previous levels academically.  That being
said, I really didn’t have enough data points to do a fair analysis or
to prove any correlations between the impacts of the Great Recession
on households and how that may have filtered down into the student’s
performances on national assessments.              

    Some of the data files were pretty simple and easy to access and some required
substantial editing and reshaping in order to make us of them.  The
data file on free lunch participation was by far the most difficult to
make use of but still provided useful information once I was able to
isolate the specific numbers for the United State as a whole.  I used
an API with the Bureau of Labor Statistics to look at ‘employment’
levels which is another measure of who has a job but the data wasn’t
any more useful than looking at the formal unemployment rate.  I used
regex to isolate information on unemployment and its impact on
students learning from a New York Times and a Time magazine article
both published shortly after the Great Recession.  While I wasn’t able
to incorporate that data into my formal analysis I thought it provided
valuable background information and context that validated the
research.  I had the most trouble getting the interactive plots with
Shiny to work but eventually I was able to successful make plots for
the national science scores and the unemployment data that displayed
the tables and allowed for some minor interactive features like typing
in a year and getting a plot for the data for that specific year.

    Overall I found the project challenging but I’m proud of the effort I
put into learning how to access various data sources and manipulate
them in ways that can allow for basic regressions and analysis.  I’m
disappointed that I wasn’t able to produce a regression that had more
valuable data but that would have required retooling the structure of
the study and finding data sources that provided more data points.
The unemployment data had almost 100 values but it was challenging to
find the equivalent test score data.  If I were to do this again I
would have expanded the analysis to include other subjects (math,
reading and social studies) and probably other grades as well.  That
would have provided me enough science data to match up with the
unemployment data and hopefully create a regression that provided more
robust results.  Ultimately though I have doubts on the validity of
the national science score results, both from this project and my own
personal experience as a middle school science teacher.  Once I finish
my classes this quarter and I have a little more free time, I plan on
exploring this topic more and to further investigate the different
ways that unemployment and other family shocks can impact a student’s
ability to learn and succeed in school.