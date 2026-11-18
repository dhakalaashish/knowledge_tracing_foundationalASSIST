# FoundationalASSIST skills and their practices

164 skill codes (Data/Skills.csv) over 3368 problems; a problem with several codes counts once under each (3717 problem–skill links). Practices: each problem's top practice from ch3 (`qwen35_122b_ch3_top_practice`). Responses: the cleaned MACA-CD data. Made by `Code/practice_analysis/skills_by_practice.js`.

## Can a skill stand for a practice?

| Verdict (majority practice of ch3) | Skills | Problems | Share of responses |
|---|---:|---:|---:|
| One practice (≥ 80% of problems) | 33 | 546 | 12.2% |
| Mostly one practice (60–80%) | 40 | 1156 | 32.5% |
| Mixed (< 60%) | 58 | 1961 | 55.0% |
| Fewer than 3 problems | 33 | 54 | 0.4% |

Giving every problem its skill's most common practice would label 59.5% of problems correctly with the ch3 labels (in sample, so optimistic; always guessing Procedural gets 46%).

## All skills

Mix = number of problems with each top practice (ch3), in the order REP / A&G / J&P / MOD / COL / PF. Majority = most common practice and its share.

| Skill | Name | Problems | Responses | Mix ch3 | Majority ch3 | Verdict |
|---|---|---:|---:|---|---|---|
| 2.MD.B.5 | Solve Word Problems Involving Lengths using Addition & Subtraction | 2 | 52 | 2 / 0 / 0 / 0 / 0 / 0 | REP 100% | too few problems |
| 3.MD.B.3 | Draw & Apply Knowledge of Bar & Pictures Graphs | 2 | 36 | 2 / 0 / 0 / 0 / 0 / 0 | REP 100% | too few problems |
| 3.MD.C.6 | Measure Area by Counting Unit Squares | 2 | 0 | 0 / 0 / 0 / 0 / 0 / 2 | PF 100% | too few problems |
| 3.MD.C.7a | Find the Area of a Rectangle by Tiling | 5 | 77 | 1 / 0 / 0 / 0 / 0 / 4 | PF 80% | one practice (PF) |
| 3.MD.C.7d | Find Area of Rectangles by Decomposing | 2 | 190 | 2 / 0 / 0 / 0 / 0 / 0 | REP 100% | too few problems |
| 3.MD.D.8 | Solve Word Problems Involving Perimeter of Polygons | 2 | 77 | 0 / 0 / 0 / 0 / 0 / 2 | PF 100% | too few problems |
| 3.NF.A.2a | Represent Unit Fractions on a Number Line | 1 | 0 | 1 / 0 / 0 / 0 / 0 / 0 | REP 100% | too few problems |
| 3.NF.A.2b | Represent Fractions on a Number Line | 5 | 0 | 5 / 0 / 0 / 0 / 0 / 0 | REP 100% | one practice (REP) |
| 3.NF.A.3b | Recognize & Generate Simple Equivalent Fractions | 1 | 0 | 1 / 0 / 0 / 0 / 0 / 0 | REP 100% | too few problems |
| 3.NF.A.3d | Comprare Fractions with Like Numerators or Denominators | 1 | 0 | 0 / 0 / 0 / 0 / 0 / 1 | PF 100% | too few problems |
| 3.OA.A.1 | Interpret Products of Whole Numbers | 2 | 52 | 2 / 0 / 0 / 0 / 0 / 0 | REP 100% | too few problems |
| 3.OA.A.4 | Determine the Unknown Whole Number in a Multiplication/Division Equation | 2 | 52 | 2 / 0 / 0 / 0 / 0 / 0 | REP 100% | too few problems |
| 3.OA.B.5 | Apply Properties of Operations To Multiply & Divide | 2 | 52 | 0 / 1 / 0 / 0 / 0 / 1 | A&G 50% | too few problems |
| 4.G.A.1 | Draw & Identify Types of Lines and Angles | 8 | 493 | 6 / 0 / 0 / 0 / 0 / 2 | REP 75% | mostly REP |
| 4.G.A.2 | Classify 2D Figures by Parallel & Perpendicular Lines and Angles | 3 | 1,345 | 2 / 1 / 0 / 0 / 0 / 0 | REP 67% | mostly REP |
| 4.MD.A.1 | Convert Measurements Within a System & Display in Two-Column Tables | 8 | 3,839 | 6 / 0 / 0 / 0 / 0 / 2 | REP 75% | mostly REP |
| 4.MD.A.3 | Apply Area & Perimeter Formulas for Rectangles | 12 | 5,639 | 1 / 0 / 0 / 0 / 0 / 11 | PF 92% | one practice (PF) |
| 4.NBT.A.1 | Recognize & Apply Concepts of Place Value Relationships | 6 | 378 | 6 / 0 / 0 / 0 / 0 / 0 | REP 100% | one practice (REP) |
| 4.NBT.B.6 | Divide Whole Numbers using Place Value Models & Strategies | 2 | 56 | 1 / 0 / 0 / 0 / 0 / 1 | REP 50% | too few problems |
| 4.NF.A.1 | Explain, Recognize & Generate Equivalent Fractions | 2 | 129 | 0 / 0 / 0 / 0 / 0 / 2 | PF 100% | too few problems |
| 4.NF.A.2 | Compare Fractions with Different Numerators & Denominators | 6 | 133 | 1 / 0 / 0 / 0 / 0 / 5 | PF 83% | one practice (PF) |
| 4.NF.B.4b | Multiply a Fraction by a Whole Number | 6 | 378 | 6 / 0 / 0 / 0 / 0 / 0 | REP 100% | one practice (REP) |
| 4.NF.C.6 | Convert Fractions to Decimals (Denominators of 10 or 100) | 6 | 814 | 4 / 0 / 0 / 0 / 0 / 2 | REP 67% | mostly REP |
| 4.OA.A.1 | Interpret & Represent Multiplicative Comparisons as Multiplication Equations | 6 | 378 | 6 / 0 / 0 / 0 / 0 / 0 | REP 100% | one practice (REP) |
| 4.OA.B.4 | Find & Use Factors of to Determine if a Number is Prime or Composite | 2 | 31 | 1 / 0 / 0 / 0 / 0 / 1 | REP 50% | too few problems |
| 5.G.A.1 | Understand Components of the Coordinate Plane | 5 | 0 | 5 / 0 / 0 / 0 / 0 / 0 | REP 100% | one practice (REP) |
| 5.G.A.2 | Graph points in Quadrant 1 & Interpret Coordinate Values | 1 | 0 | 1 / 0 / 0 / 0 / 0 / 0 | REP 100% | too few problems |
| 5.G.B.4 | Classify 2D Figures Based on Properties | 3 | 2,677 | 1 / 2 / 0 / 0 / 0 / 0 | A&G 67% | mostly A&G |
| 5.MD.A.1 | Convert Among Standard Measurement Units | 4 | 338 | 1 / 0 / 0 / 0 / 0 / 3 | PF 75% | mostly PF |
| 5.MD.B.2 | Create Line Plots with Fractions | 4 | 35 | 4 / 0 / 0 / 0 / 0 / 0 | REP 100% | one practice (REP) |
| 5.MD.C.3b | Understand that Unit Cubes Can be Used to Construct Volume | 1 | 638 | 1 / 0 / 0 / 0 / 0 / 0 | REP 100% | too few problems |
| 5.MD.C.4 | Measure Volumes with Unit Cubes | 1 | 1,092 | 0 / 0 / 0 / 0 / 0 / 1 | PF 100% | too few problems |
| 5.MD.C.5a | Find the Volume of a Rectangular Prism Without a Formula | 2 | 74 | 0 / 0 / 0 / 0 / 0 / 2 | PF 100% | too few problems |
| 5.MD.C.5b | Find the Volume of a Rectangular Prism With a Formula | 3 | 799 | 0 / 0 / 0 / 0 / 0 / 3 | PF 100% | one practice (PF) |
| 5.NBT.A.1 | Understand Base Ten Place Value Relationships | 6 | 175 | 6 / 0 / 0 / 0 / 0 / 0 | REP 100% | one practice (REP) |
| 5.NBT.A.2 | Explain Patterns when Multiplying & Dividing Powers of 10 | 2 | 953 | 1 / 0 / 0 / 0 / 0 / 1 | REP 50% | too few problems |
| 5.NBT.A.3b | Compare Decimals to Thousandths | 2 | 0 | 1 / 0 / 0 / 0 / 0 / 1 | REP 50% | too few problems |
| 5.NBT.B.5 | Multiply Multi-Digit Whole Numbers Using the Standard Algorithm | 17 | 1,213 | 1 / 0 / 0 / 0 / 1 / 15 | PF 88% | one practice (PF) |
| 5.NBT.B.6 | Divide Whole Numbers (Up to 4-Digit Dividends & 2-Digit Divisors) | 10 | 882 | 0 / 0 / 0 / 0 / 0 / 10 | PF 100% | one practice (PF) |
| 5.NBT.B.7 | Compute Decimal Problems Involving All 4 Operations | 34 | 1,038 | 2 / 1 / 0 / 0 / 0 / 31 | PF 91% | one practice (PF) |
| 5.NF.A.1 | Add & Subtract Fractions with Unlike Denominators | 3 | 1,497 | 2 / 0 / 0 / 0 / 0 / 1 | REP 67% | mostly REP |
| 5.NF.A.2 | Solve Word Problems Involving Addition/Subtraction of Fractions | 1 | 340 | 1 / 0 / 0 / 0 / 0 / 0 | REP 100% | too few problems |
| 5.NF.B.3 | Interpret Fractions as Division in Word Problems | 4 | 473 | 0 / 0 / 0 / 0 / 0 / 4 | PF 100% | one practice (PF) |
| 5.NF.B.4a | Interpret & Compute Products of Fractions and Whole Numbers | 10 | 2,175 | 0 / 0 / 0 / 0 / 0 / 10 | PF 100% | one practice (PF) |
| 5.NF.B.4b | Find the Area of a Rectangle with Fractional Side Lengths | 2 | 261 | 1 / 0 / 1 / 0 / 0 / 0 | REP 50% | too few problems |
| 5.NF.B.5a | Compare the Size of Products & Factors | 6 | 373 | 3 / 0 / 0 / 0 / 0 / 3 | REP 50% | mixed |
| 5.NF.B.5b | Explain Results Less or Greater Than 1 when Multiplying Fractions | 2 | 50 | 0 / 0 / 0 / 0 / 0 / 2 | PF 100% | too few problems |
| 5.NF.B.6 | Solve Real-World Problems Involving Multiplication of Fractions | 2 | 593 | 1 / 0 / 0 / 0 / 0 / 1 | REP 50% | too few problems |
| 5.NF.B.7a | Interpret & Compute Quotients of Unit Fractions & Whole Numbers | 1 | 32 | 1 / 0 / 0 / 0 / 0 / 0 | REP 100% | too few problems |
| 5.NF.B.7b | Interpret & Compute Quotients of Whole Numbers & Unit Fractions | 3 | 151 | 1 / 0 / 0 / 0 / 0 / 2 | PF 67% | mostly PF |
| 5.NF.B.7c | Solve Word Problems Involving Division of Fractions & Whole Numbers | 2 | 94 | 1 / 0 / 0 / 0 / 0 / 1 | REP 50% | too few problems |
| 5.OA.A.1 | Evaluate Expressions Using Groupings | 2 | 52 | 0 / 1 / 0 / 0 / 0 / 1 | A&G 50% | too few problems |
| 5.OA.A.2 | Write & Interpret Simple Expressions | 2 | 190 | 2 / 0 / 0 / 0 / 0 / 0 | REP 100% | too few problems |
| 6.EE.A.1 | Write & Evaluate Numerical Expressions with Exponents | 76 | 30,778 | 7 / 2 / 5 / 0 / 0 / 62 | PF 82% | one practice (PF) |
| 6.EE.A.2a | Write Expressions with Numbers & Variables | 8 | 3,575 | 6 / 0 / 0 / 0 / 0 / 2 | REP 75% | mostly REP |
| 6.EE.A.2b | Identify Parts of an Expression | 6 | 66 | 2 / 0 / 0 / 0 / 0 / 4 | PF 67% | mostly PF |
| 6.EE.A.2c | Evaluate Expression in Real-World Context | 22 | 12,286 | 1 / 0 / 0 / 0 / 0 / 21 | PF 95% | one practice (PF) |
| 6.EE.A.3 | Generate Equivalent Expressions using Properties of Operations | 26 | 9,270 | 8 / 1 / 0 / 0 / 0 / 17 | PF 65% | mostly PF |
| 6.EE.A.4 | Identify Equivalent Expressions | 16 | 9,473 | 3 / 1 / 2 / 0 / 0 / 10 | PF 63% | mostly PF |
| 6.EE.B.5 | Solve 1-Step Equations & Inequalities Using Substitution | 29 | 22,204 | 2 / 0 / 0 / 0 / 1 / 26 | PF 90% | one practice (PF) |
| 6.EE.B.6 | Write Expressions with Variables to Solve Problems | 48 | 23,150 | 29 / 0 / 0 / 2 / 0 / 17 | REP 60% | mostly REP |
| 6.EE.B.7 | Write & Solve 1-Step Equations | 78 | 41,255 | 30 / 0 / 0 / 0 / 0 / 48 | PF 62% | mostly PF |
| 6.EE.B.8 | Write Simple Inequalities to Represent a Condition | 16 | 9,112 | 3 / 1 / 4 / 1 / 0 / 7 | PF 44% | mixed |
| 6.EE.C.9 | Write & Analyze Relationships Between Dependent & Independent Variables | 18 | 6,803 | 6 / 2 / 0 / 6 / 0 / 4 | REP 33% | mixed |
| 6.G.A.1 | Find the Area of Triangles, Quadrilaterals & Polygons | 111 | 62,549 | 72 / 3 / 5 / 0 / 0 / 31 | REP 65% | mostly REP |
| 6.G.A.2 | Find the Volume of Rectangular Prisms with Fractional Sides | 30 | 6,713 | 6 / 0 / 1 / 1 / 0 / 22 | PF 73% | mostly PF |
| 6.G.A.3 | Use Coordinates on a Graph to Create Polygons & Find Side Lengths | 6 | 2,256 | 1 / 0 / 0 / 0 / 0 / 5 | PF 83% | one practice (PF) |
| 6.G.A.4 | Represent 3D Figures Using Nets to Find Surface Area | 43 | 19,931 | 18 / 6 / 2 / 0 / 0 / 17 | REP 42% | mixed |
| 6.NS.A.1 | Interpret & Compute using Division of Fractions | 146 | 66,126 | 63 / 1 / 3 / 8 / 3 / 68 | PF 47% | mixed |
| 6.NS.B.2 | Divide Multi-Digit Whole Numbers | 29 | 9,738 | 2 / 0 / 1 / 1 / 1 / 24 | PF 83% | one practice (PF) |
| 6.NS.B.3 | Add, Subtract, Multiply & Divide Multi-Digit Decimals | 126 | 45,148 | 18 / 4 / 2 / 6 / 1 / 95 | PF 75% | mostly PF |
| 6.NS.B.4 | Find Common Factors & Multiples | 29 | 6,430 | 1 / 2 / 0 / 4 / 0 / 22 | PF 76% | mostly PF |
| 6.NS.C.5 | Use Positive & Negative Numbers to Represent Quantities | 37 | 15,155 | 24 / 2 / 1 / 2 / 0 / 8 | REP 65% | mostly REP |
| 6.NS.C.6a | Identify Opposites of Integers | 6 | 4,365 | 5 / 0 / 1 / 0 / 0 / 0 | REP 83% | one practice (REP) |
| 6.NS.C.6c | Plot Integers Points on a Number Line & Coordinate Planes | 14 | 5,430 | 9 / 0 / 0 / 0 / 0 / 5 | REP 64% | mostly REP |
| 6.NS.C.7a | Interpret & Compare Integers Using a Number Line | 17 | 10,422 | 5 / 0 / 0 / 0 / 1 / 11 | PF 65% | mostly PF |
| 6.NS.C.7b | Interpret & Compare Rational Numbers in Real-World Contexts | 10 | 5,083 | 1 / 0 / 0 / 0 / 1 / 8 | PF 80% | one practice (PF) |
| 6.NS.C.7c | Understand & Interpret Absolute Value | 7 | 1,972 | 2 / 0 / 0 / 0 / 0 / 5 | PF 71% | mostly PF |
| 6.NS.C.7d | Understand & Interpret Absolute Value in Real-World Contexts | 2 | 940 | 1 / 0 / 0 / 0 / 1 / 0 | REP 50% | too few problems |
| 6.NS.C.8 | Solve Real-World Problems by Graphing on a Coordinate Plane | 14 | 3,480 | 8 / 0 / 0 / 0 / 0 / 6 | REP 57% | mixed |
| 6.RP.A.1 | Understand & Describe Ratios | 11 | 8,047 | 4 / 1 / 0 / 0 / 0 / 6 | PF 55% | mixed |
| 6.RP.A.2 | Understand & Describe Unit Rate | 19 | 1,794 | 13 / 1 / 0 / 0 / 0 / 5 | REP 68% | mostly REP |
| 6.RP.A.3a | Create Tables to Compare Equivalent Ratios | 74 | 34,679 | 28 / 4 / 1 / 6 / 1 / 34 | PF 46% | mixed |
| 6.RP.A.3b | Solve Unit Rate Problems | 146 | 94,527 | 88 / 2 / 1 / 21 / 0 / 34 | REP 60% | mostly REP |
| 6.RP.A.3c | Solve Problems Involving Percents | 147 | 78,188 | 87 / 3 / 1 / 1 / 2 / 53 | REP 59% | mixed |
| 6.RP.A.3d | Use Ratios to Convert Measurement Units | 30 | 17,532 | 5 / 2 / 1 / 1 / 0 / 21 | PF 70% | mostly PF |
| 6.SP.A.1 | Recognize Statistical Questions Account for Variablility | 9 | 1,922 | 2 / 1 / 0 / 4 / 1 / 1 | MOD 44% | mixed |
| 6.SP.A.2 | Understand Properties of Distribution with (or for) Data | 5 | 1,425 | 2 / 2 / 0 / 1 / 0 / 0 | REP 40% | mixed |
| 6.SP.A.3 | Recognize Properties of Measure of Center with Variation | 7 | 811 | 0 / 1 / 0 / 0 / 0 / 6 | PF 86% | one practice (PF) |
| 6.SP.B.4 | Display Numerical Data Using Dot Plots, Histograms & Box Plots | 26 | 6,796 | 15 / 6 / 3 / 0 / 0 / 2 | REP 58% | mixed |
| 6.SP.B.5a | Report the Number of Observations in a Data Set | 1 | 0 | 1 / 0 / 0 / 0 / 0 / 0 | REP 100% | too few problems |
| 6.SP.B.5b | Describe the Attributes of a Data Set | 7 | 1,984 | 3 / 0 / 0 / 1 / 0 / 3 | REP 43% | mixed |
| 6.SP.B.5c | Give & Describe Quantitative Measures of Center & Variability | 62 | 11,818 | 13 / 9 / 5 / 2 / 0 / 33 | PF 53% | mixed |
| 6.SP.B.5d | Relate Measures of Center & Variablity to Distribution of Data | 4 | 221 | 1 / 2 / 0 / 0 / 0 / 1 | A&G 50% | mixed |
| 7.EE.A.1 | Apply Properties of Operations to Create Equivalent Expressions | 24 | 16,756 | 0 / 1 / 3 / 0 / 1 / 19 | PF 79% | mostly PF |
| 7.EE.A.2 | Understand Equivalent Expressions in Context | 13 | 11,367 | 7 / 1 / 1 / 0 / 0 / 4 | REP 54% | mixed |
| 7.EE.B.3 | Solve Applied Problems Using Numerical and Algebraic Expressions and Equations | 25 | 3,621 | 20 / 0 / 0 / 5 / 0 / 0 | REP 80% | one practice (REP) |
| 7.EE.B.4a | Solve 2-Step Equations | 107 | 80,067 | 33 / 2 / 1 / 4 / 0 / 67 | PF 63% | mostly PF |
| 7.EE.B.4b | Solve, Graph & Interpret 2-Step Inequalities | 28 | 19,232 | 4 / 0 / 1 / 4 / 1 / 18 | PF 64% | mostly PF |
| 7.G.A.1 | Solve Scale Drawing Problems | 113 | 87,120 | 36 / 31 / 5 / 4 / 2 / 35 | REP 32% | mixed |
| 7.G.A.2 | Draw Geometric Shapes & Unique Triangles | 25 | 10,653 | 4 / 3 / 9 / 1 / 0 / 8 | J&P 36% | mixed |
| 7.G.A.3 | Describe 2D Cross Sections of 3D figures | 8 | 1,709 | 4 / 1 / 0 / 0 / 0 / 3 | REP 50% | mixed |
| 7.G.B.4 | Solve Problems Involving Area & Circumference of Circles | 105 | 83,004 | 48 / 6 / 4 / 10 / 0 / 37 | REP 46% | mixed |
| 7.G.B.5 | Use Facts About Angles to Write & Solve Equations | 44 | 26,337 | 23 / 1 / 3 / 0 / 1 / 16 | REP 52% | mixed |
| 7.G.B.6 | Find Area, Volume & Surface Area of 2D/3D Objects | 64 | 34,048 | 27 / 2 / 1 / 9 / 0 / 25 | REP 42% | mixed |
| 7.NS.A.1a | Describe Situations Where Opposite Quantities Combine to Make 0 | 1 | 33 | 0 / 0 / 0 / 0 / 0 / 1 | PF 100% | too few problems |
| 7.NS.A.1b | Interpret Sums of Rational Numbers | 10 | 7,490 | 6 / 0 / 1 / 1 / 0 / 2 | REP 60% | mostly REP |
| 7.NS.A.1c | Understand Properties of Subtracting Rational Numbers | 9 | 4,471 | 2 / 1 / 1 / 0 / 0 / 5 | PF 56% | mixed |
| 7.NS.A.1d | Apply Properties of Operations to Add/Subtract Rational Numbers | 41 | 37,450 | 8 / 0 / 0 / 4 / 0 / 29 | PF 71% | mostly PF |
| 7.NS.A.2a | Understand Applied Context for Multiplying Rational Numbers | 6 | 3,671 | 1 / 0 / 0 / 0 / 0 / 5 | PF 83% | one practice (PF) |
| 7.NS.A.2b | Understand Applied Context for Dividing Rational Numbers | 9 | 970 | 1 / 2 / 0 / 1 / 0 / 5 | PF 56% | mixed |
| 7.NS.A.2c | Apply Properties of Operations to Multiply/Divide Rational Numbers | 47 | 49,156 | 3 / 1 / 0 / 0 / 0 / 43 | PF 91% | one practice (PF) |
| 7.NS.A.2d | Convert a Rational Number to a Decimal | 10 | 3,864 | 1 / 0 / 1 / 0 / 0 / 8 | PF 80% | one practice (PF) |
| 7.NS.A.3 | Solve Applied Problems Involving All Operations of Rational Numbers | 8 | 1,817 | 0 / 0 / 0 / 0 / 0 / 8 | PF 100% | one practice (PF) |
| 7.RP.A.1 | Compute Unit Rates with Fractions | 16 | 15,794 | 6 / 0 / 0 / 1 / 0 / 9 | PF 56% | mixed |
| 7.RP.A.2a | Identify Proportional Relationships | 111 | 67,238 | 40 / 27 / 3 / 19 / 0 / 22 | REP 36% | mixed |
| 7.RP.A.2b | Identify the Constant of Proportionality | 24 | 26,998 | 6 / 10 / 1 / 1 / 1 / 5 | A&G 42% | mixed |
| 7.RP.A.2c | Represent Proportional Relationships with Equations | 56 | 54,757 | 30 / 9 / 3 / 3 / 0 / 11 | REP 54% | mixed |
| 7.RP.A.2d | Interpret Points on Proportional Graphs | 7 | 653 | 4 / 2 / 0 / 0 / 0 / 1 | REP 57% | mixed |
| 7.RP.A.3 | Use Proportional Relationships to Solve Ratio & Percent Problems | 198 | 127,884 | 98 / 13 / 2 / 28 / 1 / 56 | REP 49% | mixed |
| 7.SP.A.1 | Interpret Methods of Sampling | 11 | 2,274 | 0 / 3 / 5 / 3 / 0 / 0 | J&P 45% | mixed |
| 7.SP.A.2 | Use Random Samples to Draw Influences | 22 | 2,191 | 4 / 8 / 1 / 4 / 1 / 4 | A&G 36% | mixed |
| 7.SP.B.3 | Compare Populations using Center & Variability | 12 | 1,533 | 2 / 4 / 3 / 0 / 0 / 3 | A&G 33% | mixed |
| 7.SP.B.4 | Draw Inferences using Measures of Center & Variability | 27 | 3,186 | 4 / 7 / 4 / 3 / 0 / 9 | PF 33% | mixed |
| 7.SP.C.5 | Understand that Probability is Between 0-1 & Describes the Likelihood of an Event Occurring | 20 | 3,762 | 6 / 0 / 1 / 6 / 0 / 7 | PF 35% | mixed |
| 7.SP.C.6 | Approximate Probability of an Event by Collecting Data | 10 | 2,800 | 5 / 0 / 3 / 0 / 0 / 2 | REP 50% | mixed |
| 7.SP.C.7a | Develop a Uniform Probabilty Model of a Single Event | 8 | 2,262 | 3 / 2 / 0 / 1 / 0 / 2 | REP 38% | mixed |
| 7.SP.C.7b | Develop a Probability Model of a Single Event | 5 | 2,032 | 0 / 1 / 0 / 3 / 0 / 1 | MOD 60% | mostly MOD |
| 7.SP.C.8a | Understand Probability of a Compound Event | 8 | 1,830 | 3 / 0 / 0 / 0 / 0 / 5 | PF 63% | mostly PF |
| 7.SP.C.8b | Represent Sample Spaces for Compound Events | 21 | 7,378 | 8 / 0 / 1 / 3 / 0 / 9 | PF 43% | mixed |
| 7.SP.C.8c | Design & Use a Simulation for Compound Events | 7 | 2,330 | 3 / 0 / 0 / 3 / 1 / 0 | REP 43% | mixed |
| 8.EE.A.1 | Know & Apply Properties of Exponents | 29 | 8,989 | 0 / 4 / 2 / 0 / 0 / 23 | PF 79% | mostly PF |
| 8.EE.A.2 | Evaluate Square & Cube Roots | 33 | 11,401 | 0 / 0 / 0 / 0 / 0 / 33 | PF 100% | one practice (PF) |
| 8.EE.A.3 | Expressing Quantities in Scientific Notation | 15 | 4,190 | 6 / 4 / 0 / 0 / 0 / 5 | REP 40% | mixed |
| 8.EE.A.4 | Apply Scientific Notation Operations | 31 | 2,096 | 8 / 0 / 0 / 3 / 0 / 20 | PF 65% | mostly PF |
| 8.EE.B.5 | Compare Slopes of Proportional Relationships | 11 | 1,519 | 8 / 1 / 0 / 0 / 0 / 2 | REP 73% | mostly REP |
| 8.EE.B.6 | Find Slope of a Line using Similar Triangles | 25 | 8,603 | 14 / 4 / 0 / 1 / 0 / 6 | REP 56% | mixed |
| 8.EE.C.7a | Solve Linear Equations with One, Multiple or No Solutions | 20 | 8,962 | 4 / 4 / 6 / 0 / 1 / 5 | J&P 30% | mixed |
| 8.EE.C.7b | Solve Multi-Step Linear Equations with Rational Number Coefficients | 60 | 32,405 | 7 / 1 / 2 / 1 / 0 / 49 | PF 82% | one practice (PF) |
| 8.EE.C.8a | Identify Solutions to Systems of Equations Using Graphs | 21 | 4,964 | 13 / 1 / 5 / 0 / 0 / 2 | REP 62% | mostly REP |
| 8.EE.C.8b | Solve Systems of Linear Equations Algebraically | 9 | 5,246 | 1 / 0 / 0 / 1 / 0 / 7 | PF 78% | mostly PF |
| 8.EE.C.8c | Solve Systems of Linear Equations Word Problems | 21 | 11,566 | 11 / 0 / 0 / 6 / 0 / 4 | REP 52% | mixed |
| 8.F.A.1 | Understand Definition of a Function | 14 | 5,559 | 2 / 3 / 3 / 0 / 0 / 6 | PF 43% | mixed |
| 8.F.A.2 | Compare Functions in Different Forms | 3 | 754 | 2 / 0 / 0 / 0 / 0 / 1 | REP 67% | mostly REP |
| 8.F.A.3 | Identify Linear & Non-Linear Functions | 11 | 2,101 | 3 / 3 / 0 / 0 / 0 / 5 | PF 45% | mixed |
| 8.F.B.4 | Use Functions to Model Relationships Between Quantities | 57 | 22,351 | 23 / 10 / 1 / 4 / 0 / 19 | REP 40% | mixed |
| 8.F.B.5 | Qualitatively Describe & Graph Relationships | 22 | 4,343 | 18 / 1 / 1 / 1 / 0 / 1 | REP 82% | one practice (REP) |
| 8.G.A.1a | Apply Properties of Transformations to Lines & Line Segments | 10 | 1,041 | 1 / 2 / 2 / 0 / 0 / 5 | PF 50% | mixed |
| 8.G.A.1b | Apply the Properties of Transformations to Angles | 24 | 6,088 | 8 / 3 / 1 / 0 / 0 / 12 | PF 50% | mixed |
| 8.G.A.1c | Apply the Properties of Transformations to Parallel Lines | 1 | 31 | 0 / 1 / 0 / 0 / 0 / 0 | A&G 100% | too few problems |
| 8.G.A.2 | Understand & Describe Geometric Transformation Sequences | 21 | 3,457 | 7 / 1 / 5 / 0 / 0 / 8 | PF 38% | mixed |
| 8.G.A.3 | Describe the Effect of Transformations on 2D Figures | 14 | 5,824 | 2 / 4 / 1 / 0 / 0 / 7 | PF 50% | mixed |
| 8.G.A.4 | use Transformations to Determine Similarity in 2D figures | 18 | 6,512 | 8 / 2 / 6 / 0 / 0 / 2 | REP 44% | mixed |
| 8.G.A.5 | Use Informal Arguments to Establish Facts about Angles for Similar Triangles | 10 | 3,354 | 2 / 1 / 2 / 0 / 0 / 5 | PF 50% | mixed |
| 8.G.B.6 | Prove the Pythagorean Theorem & it's Converse | 1 | 166 | 0 / 0 / 0 / 0 / 0 / 1 | PF 100% | too few problems |
| 8.G.B.7 | Apply the Pythagorean Theorem to 2D & 3D FIgures | 38 | 8,846 | 12 / 1 / 1 / 4 / 1 / 19 | PF 50% | mixed |
| 8.G.B.8 | Apply the Pythagorean Theorem to Find the Distance Between Points on the Coordinate Plane | 11 | 398 | 1 / 0 / 0 / 0 / 0 / 10 | PF 91% | one practice (PF) |
| 8.G.C.9 | Know & Use Volume Formulas | 92 | 23,400 | 26 / 8 / 0 / 3 / 0 / 55 | PF 60% | mixed |
| 8.NS.A.1 | Understand & Approximate Rational & Irrational Numbers | 9 | 739 | 4 / 0 / 3 / 0 / 0 / 2 | REP 44% | mixed |
| 8.NS.A.2 | Approximate Irrational Numbers | 28 | 10,227 | 6 / 0 / 0 / 1 / 0 / 21 | PF 75% | mostly PF |
| 8.SP.A.1 | Construct & Interpret Scatter Plots | 16 | 3,405 | 7 / 8 / 0 / 1 / 0 / 0 | A&G 50% | mixed |
| 8.SP.A.2 | Determine Line of Best Fit for Scatter Plots | 11 | 1,520 | 4 / 0 / 0 / 5 / 2 / 0 | MOD 45% | mixed |
| 8.SP.A.3 | Use Linear Equations Applied to Bivariate Data | 15 | 1,951 | 9 / 0 / 0 / 3 / 0 / 3 | REP 60% | mostly REP |
| 8.SP.A.4 | Construct & Interpret Two Way Tables | 7 | 612 | 0 / 1 / 2 / 2 / 0 / 2 | J&P 29% | mixed |
