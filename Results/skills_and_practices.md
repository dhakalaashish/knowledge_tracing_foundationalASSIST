# FoundationalASSIST skills and their practices

164 skill codes (Data/Skills.csv) over 3368 problems; a problem with several codes counts once under each (3717 problem–skill links). Practices: each problem's top practice from Qwen v3 and Qwen v4. Responses: the cleaned MACA-CD data. Made by `Code/practice_analysis/skills_by_practice.js`.

## Can a skill stand for a practice?

| Verdict (both v3 and v4 agree on the majority practice) | Skills | Problems | Share of responses |
|---|---:|---:|---:|
| One practice (≥ 80% of problems) | 14 | 198 | 4.7% |
| Mostly one practice (60–80%) | 37 | 965 | 24.0% |
| Mixed (< 60%, or v3 and v4 disagree) | 80 | 2500 | 71.0% |
| Fewer than 3 problems | 33 | 54 | 0.4% |

Giving every problem its skill's most common practice would label 56.6% of problems correctly with the v3 labels and 63.9% with v4 (in sample, so optimistic; always guessing Procedural gets about 48%).

## All skills

Mix = number of problems with each top practice (v3), in the order REP / A&G / J&P / MOD / COL / PF. Majority = most common practice and its share.

| Skill | Name | Problems | Responses | Mix v3 | Majority v3 | Majority v4 | Verdict |
|---|---|---:|---:|---|---|---|---|
| 2.MD.B.5 | Solve Word Problems Involving Lengths using Addition & Subtraction | 2 | 52 | 0 / 0 / 2 / 0 / 0 / 0 | J&P 100% | REP 50% | too few problems |
| 3.MD.B.3 | Draw & Apply Knowledge of Bar & Pictures Graphs | 2 | 36 | 1 / 0 / 1 / 0 / 0 / 0 | REP 50% | REP 100% | too few problems |
| 3.MD.C.6 | Measure Area by Counting Unit Squares | 2 | 0 | 1 / 0 / 0 / 0 / 0 / 1 | REP 50% | PF 100% | too few problems |
| 3.MD.C.7a | Find the Area of a Rectangle by Tiling | 5 | 77 | 1 / 0 / 1 / 0 / 0 / 3 | PF 60% | PF 80% | mostly PF |
| 3.MD.C.7d | Find Area of Rectangles by Decomposing | 2 | 190 | 0 / 0 / 2 / 0 / 0 / 0 | J&P 100% | REP 50% | too few problems |
| 3.MD.D.8 | Solve Word Problems Involving Perimeter of Polygons | 2 | 77 | 0 / 0 / 0 / 0 / 0 / 2 | PF 100% | PF 100% | too few problems |
| 3.NF.A.2a | Represent Unit Fractions on a Number Line | 1 | 0 | 1 / 0 / 0 / 0 / 0 / 0 | REP 100% | REP 100% | too few problems |
| 3.NF.A.2b | Represent Fractions on a Number Line | 5 | 0 | 5 / 0 / 0 / 0 / 0 / 0 | REP 100% | REP 100% | one practice (REP) |
| 3.NF.A.3b | Recognize & Generate Simple Equivalent Fractions | 1 | 0 | 1 / 0 / 0 / 0 / 0 / 0 | REP 100% | REP 100% | too few problems |
| 3.NF.A.3d | Comprare Fractions with Like Numerators or Denominators | 1 | 0 | 0 / 0 / 0 / 0 / 0 / 1 | PF 100% | J&P 100% | too few problems |
| 3.OA.A.1 | Interpret Products of Whole Numbers | 2 | 52 | 1 / 0 / 1 / 0 / 0 / 0 | REP 50% | J&P 50% | too few problems |
| 3.OA.A.4 | Determine the Unknown Whole Number in a Multiplication/Division Equation | 2 | 52 | 1 / 0 / 1 / 0 / 0 / 0 | REP 50% | J&P 50% | too few problems |
| 3.OA.B.5 | Apply Properties of Operations To Multiply & Divide | 2 | 52 | 0 / 0 / 2 / 0 / 0 / 0 | J&P 100% | A&G 100% | too few problems |
| 4.G.A.1 | Draw & Identify Types of Lines and Angles | 8 | 493 | 0 / 0 / 6 / 0 / 0 / 2 | J&P 75% | J&P 75% | mostly J&P |
| 4.G.A.2 | Classify 2D Figures by Parallel & Perpendicular Lines and Angles | 3 | 1,345 | 0 / 0 / 3 / 0 / 0 / 0 | J&P 100% | J&P 100% | one practice (J&P) |
| 4.MD.A.1 | Convert Measurements Within a System & Display in Two-Column Tables | 8 | 3,839 | 7 / 0 / 0 / 0 / 0 / 1 | REP 88% | REP 75% | mostly REP |
| 4.MD.A.3 | Apply Area & Perimeter Formulas for Rectangles | 12 | 5,639 | 5 / 0 / 0 / 0 / 0 / 7 | PF 58% | PF 83% | mixed |
| 4.NBT.A.1 | Recognize & Apply Concepts of Place Value Relationships | 6 | 378 | 4 / 0 / 0 / 0 / 0 / 2 | REP 67% | PF 83% | mixed |
| 4.NBT.B.6 | Divide Whole Numbers using Place Value Models & Strategies | 2 | 56 | 1 / 0 / 0 / 0 / 0 / 1 | REP 50% | PF 100% | too few problems |
| 4.NF.A.1 | Explain, Recognize & Generate Equivalent Fractions | 2 | 129 | 0 / 0 / 0 / 0 / 0 / 2 | PF 100% | J&P 50% | too few problems |
| 4.NF.A.2 | Compare Fractions with Different Numerators & Denominators | 6 | 133 | 1 / 0 / 2 / 0 / 0 / 3 | PF 50% | J&P 50% | mixed |
| 4.NF.B.4b | Multiply a Fraction by a Whole Number | 6 | 378 | 4 / 0 / 0 / 0 / 0 / 2 | REP 67% | PF 83% | mixed |
| 4.NF.C.6 | Convert Fractions to Decimals (Denominators of 10 or 100) | 6 | 814 | 4 / 0 / 1 / 0 / 0 / 1 | REP 67% | REP 67% | mostly REP |
| 4.OA.A.1 | Interpret & Represent Multiplicative Comparisons as Multiplication Equations | 6 | 378 | 4 / 0 / 0 / 0 / 0 / 2 | REP 67% | PF 83% | mixed |
| 4.OA.B.4 | Find & Use Factors of to Determine if a Number is Prime or Composite | 2 | 31 | 0 / 0 / 2 / 0 / 0 / 0 | J&P 100% | J&P 100% | too few problems |
| 5.G.A.1 | Understand Components of the Coordinate Plane | 5 | 0 | 1 / 0 / 0 / 0 / 0 / 4 | PF 80% | PF 60% | mostly PF |
| 5.G.A.2 | Graph points in Quadrant 1 & Interpret Coordinate Values | 1 | 0 | 1 / 0 / 0 / 0 / 0 / 0 | REP 100% | REP 100% | too few problems |
| 5.G.B.4 | Classify 2D Figures Based on Properties | 3 | 2,677 | 0 / 0 / 3 / 0 / 0 / 0 | J&P 100% | J&P 100% | one practice (J&P) |
| 5.MD.A.1 | Convert Among Standard Measurement Units | 4 | 338 | 1 / 0 / 0 / 0 / 0 / 3 | PF 75% | PF 75% | mostly PF |
| 5.MD.B.2 | Create Line Plots with Fractions | 4 | 35 | 0 / 0 / 4 / 0 / 0 / 0 | J&P 100% | J&P 75% | mostly J&P |
| 5.MD.C.3b | Understand that Unit Cubes Can be Used to Construct Volume | 1 | 638 | 0 / 1 / 0 / 0 / 0 / 0 | A&G 100% | PF 100% | too few problems |
| 5.MD.C.4 | Measure Volumes with Unit Cubes | 1 | 1,092 | 0 / 0 / 0 / 0 / 0 / 1 | PF 100% | PF 100% | too few problems |
| 5.MD.C.5a | Find the Volume of a Rectangular Prism Without a Formula | 2 | 74 | 1 / 0 / 0 / 0 / 0 / 1 | REP 50% | REP 100% | too few problems |
| 5.MD.C.5b | Find the Volume of a Rectangular Prism With a Formula | 3 | 799 | 0 / 0 / 1 / 0 / 0 / 2 | PF 67% | PF 100% | mostly PF |
| 5.NBT.A.1 | Understand Base Ten Place Value Relationships | 6 | 175 | 3 / 2 / 0 / 0 / 0 / 1 | REP 50% | A&G 67% | mixed |
| 5.NBT.A.2 | Explain Patterns when Multiplying & Dividing Powers of 10 | 2 | 953 | 1 / 0 / 0 / 0 / 0 / 1 | REP 50% | PF 100% | too few problems |
| 5.NBT.A.3b | Compare Decimals to Thousandths | 2 | 0 | 1 / 0 / 0 / 0 / 0 / 1 | REP 50% | REP 50% | too few problems |
| 5.NBT.B.5 | Multiply Multi-Digit Whole Numbers Using the Standard Algorithm | 17 | 1,213 | 2 / 1 / 1 / 0 / 0 / 13 | PF 76% | PF 82% | mostly PF |
| 5.NBT.B.6 | Divide Whole Numbers (Up to 4-Digit Dividends & 2-Digit Divisors) | 10 | 882 | 0 / 0 / 0 / 0 / 0 / 10 | PF 100% | PF 100% | one practice (PF) |
| 5.NBT.B.7 | Compute Decimal Problems Involving All 4 Operations | 34 | 1,038 | 0 / 1 / 2 / 0 / 0 / 31 | PF 91% | PF 91% | one practice (PF) |
| 5.NF.A.1 | Add & Subtract Fractions with Unlike Denominators | 3 | 1,497 | 0 / 0 / 2 / 0 / 0 / 1 | J&P 67% | J&P 67% | mostly J&P |
| 5.NF.A.2 | Solve Word Problems Involving Addition/Subtraction of Fractions | 1 | 340 | 0 / 0 / 1 / 0 / 0 / 0 | J&P 100% | J&P 100% | too few problems |
| 5.NF.B.3 | Interpret Fractions as Division in Word Problems | 4 | 473 | 1 / 0 / 0 / 0 / 0 / 3 | PF 75% | PF 75% | mostly PF |
| 5.NF.B.4a | Interpret & Compute Products of Fractions and Whole Numbers | 10 | 2,175 | 0 / 0 / 3 / 0 / 0 / 7 | PF 70% | PF 90% | mostly PF |
| 5.NF.B.4b | Find the Area of a Rectangle with Fractional Side Lengths | 2 | 261 | 1 / 0 / 1 / 0 / 0 / 0 | REP 50% | REP 50% | too few problems |
| 5.NF.B.5a | Compare the Size of Products & Factors | 6 | 373 | 4 / 0 / 2 / 0 / 0 / 0 | REP 67% | REP 33% | mixed |
| 5.NF.B.5b | Explain Results Less or Greater Than 1 when Multiplying Fractions | 2 | 50 | 0 / 0 / 2 / 0 / 0 / 0 | J&P 100% | J&P 100% | too few problems |
| 5.NF.B.6 | Solve Real-World Problems Involving Multiplication of Fractions | 2 | 593 | 1 / 0 / 1 / 0 / 0 / 0 | REP 50% | REP 50% | too few problems |
| 5.NF.B.7a | Interpret & Compute Quotients of Unit Fractions & Whole Numbers | 1 | 32 | 1 / 0 / 0 / 0 / 0 / 0 | REP 100% | PF 100% | too few problems |
| 5.NF.B.7b | Interpret & Compute Quotients of Whole Numbers & Unit Fractions | 3 | 151 | 2 / 0 / 0 / 0 / 0 / 1 | REP 67% | PF 100% | mixed |
| 5.NF.B.7c | Solve Word Problems Involving Division of Fractions & Whole Numbers | 2 | 94 | 2 / 0 / 0 / 0 / 0 / 0 | REP 100% | PF 100% | too few problems |
| 5.OA.A.1 | Evaluate Expressions Using Groupings | 2 | 52 | 0 / 0 / 2 / 0 / 0 / 0 | J&P 100% | A&G 100% | too few problems |
| 5.OA.A.2 | Write & Interpret Simple Expressions | 2 | 190 | 0 / 0 / 2 / 0 / 0 / 0 | J&P 100% | REP 50% | too few problems |
| 6.EE.A.1 | Write & Evaluate Numerical Expressions with Exponents | 76 | 30,778 | 9 / 5 / 9 / 0 / 0 / 53 | PF 70% | PF 75% | mostly PF |
| 6.EE.A.2a | Write Expressions with Numbers & Variables | 8 | 3,575 | 5 / 0 / 2 / 0 / 0 / 1 | REP 63% | REP 63% | mostly REP |
| 6.EE.A.2b | Identify Parts of an Expression | 6 | 66 | 4 / 2 / 0 / 0 / 0 / 0 | REP 67% | REP 33% | mixed |
| 6.EE.A.2c | Evaluate Expression in Real-World Context | 22 | 12,286 | 2 / 0 / 0 / 0 / 0 / 20 | PF 91% | PF 95% | one practice (PF) |
| 6.EE.A.3 | Generate Equivalent Expressions using Properties of Operations | 26 | 9,270 | 2 / 5 / 9 / 0 / 0 / 10 | PF 38% | PF 42% | mixed |
| 6.EE.A.4 | Identify Equivalent Expressions | 16 | 9,473 | 2 / 0 / 5 / 0 / 0 / 9 | PF 56% | PF 69% | mixed |
| 6.EE.B.5 | Solve 1-Step Equations & Inequalities Using Substitution | 29 | 22,204 | 5 / 0 / 2 / 0 / 0 / 22 | PF 76% | PF 90% | mostly PF |
| 6.EE.B.6 | Write Expressions with Variables to Solve Problems | 48 | 23,150 | 25 / 2 / 7 / 0 / 0 / 14 | REP 52% | REP 50% | mixed |
| 6.EE.B.7 | Write & Solve 1-Step Equations | 78 | 41,255 | 30 / 1 / 6 / 0 / 0 / 41 | PF 53% | PF 69% | mixed |
| 6.EE.B.8 | Write Simple Inequalities to Represent a Condition | 16 | 9,112 | 0 / 1 / 10 / 0 / 0 / 5 | J&P 63% | J&P 75% | mostly J&P |
| 6.EE.C.9 | Write & Analyze Relationships Between Dependent & Independent Variables | 18 | 6,803 | 6 / 7 / 0 / 0 / 0 / 5 | A&G 39% | PF 39% | mixed |
| 6.G.A.1 | Find the Area of Triangles, Quadrilaterals & Polygons | 111 | 62,549 | 40 / 1 / 18 / 0 / 0 / 52 | PF 47% | PF 53% | mixed |
| 6.G.A.2 | Find the Volume of Rectangular Prisms with Fractional Sides | 30 | 6,713 | 7 / 0 / 2 / 0 / 0 / 21 | PF 70% | PF 77% | mostly PF |
| 6.G.A.3 | Use Coordinates on a Graph to Create Polygons & Find Side Lengths | 6 | 2,256 | 3 / 0 / 0 / 0 / 0 / 3 | REP 50% | PF 67% | mixed |
| 6.G.A.4 | Represent 3D Figures Using Nets to Find Surface Area | 43 | 19,931 | 12 / 5 / 15 / 0 / 0 / 11 | J&P 35% | PF 44% | mixed |
| 6.NS.A.1 | Interpret & Compute using Division of Fractions | 146 | 66,126 | 40 / 1 / 19 / 0 / 0 / 86 | PF 59% | PF 77% | mixed |
| 6.NS.B.2 | Divide Multi-Digit Whole Numbers | 29 | 9,738 | 6 / 0 / 1 / 0 / 0 / 22 | PF 76% | PF 90% | mostly PF |
| 6.NS.B.3 | Add, Subtract, Multiply & Divide Multi-Digit Decimals | 126 | 45,148 | 14 / 4 / 11 / 5 / 0 / 92 | PF 73% | PF 83% | mostly PF |
| 6.NS.B.4 | Find Common Factors & Multiples | 29 | 6,430 | 2 / 0 / 6 / 0 / 0 / 21 | PF 72% | PF 76% | mostly PF |
| 6.NS.C.5 | Use Positive & Negative Numbers to Represent Quantities | 37 | 15,155 | 22 / 0 / 9 / 0 / 0 / 6 | REP 59% | REP 51% | mixed |
| 6.NS.C.6a | Identify Opposites of Integers | 6 | 4,365 | 5 / 1 / 0 / 0 / 0 / 0 | REP 83% | REP 83% | one practice (REP) |
| 6.NS.C.6c | Plot Integers Points on a Number Line & Coordinate Planes | 14 | 5,430 | 6 / 1 / 0 / 0 / 0 / 7 | PF 50% | PF 57% | mixed |
| 6.NS.C.7a | Interpret & Compare Integers Using a Number Line | 17 | 10,422 | 2 / 0 / 4 / 0 / 0 / 11 | PF 65% | J&P 47% | mixed |
| 6.NS.C.7b | Interpret & Compare Rational Numbers in Real-World Contexts | 10 | 5,083 | 2 / 1 / 5 / 0 / 0 / 2 | J&P 50% | J&P 40% | mixed |
| 6.NS.C.7c | Understand & Interpret Absolute Value | 7 | 1,972 | 1 / 0 / 0 / 0 / 0 / 6 | PF 86% | REP 43% | mixed |
| 6.NS.C.7d | Understand & Interpret Absolute Value in Real-World Contexts | 2 | 940 | 1 / 0 / 1 / 0 / 0 / 0 | REP 50% | REP 50% | too few problems |
| 6.NS.C.8 | Solve Real-World Problems by Graphing on a Coordinate Plane | 14 | 3,480 | 5 / 0 / 0 / 0 / 0 / 9 | PF 64% | PF 79% | mostly PF |
| 6.RP.A.1 | Understand & Describe Ratios | 11 | 8,047 | 1 / 0 / 7 / 0 / 0 / 3 | J&P 64% | J&P 45% | mixed |
| 6.RP.A.2 | Understand & Describe Unit Rate | 19 | 1,794 | 11 / 0 / 1 / 0 / 0 / 7 | REP 58% | PF 68% | mixed |
| 6.RP.A.3a | Create Tables to Compare Equivalent Ratios | 74 | 34,679 | 19 / 5 / 9 / 2 / 0 / 39 | PF 53% | PF 54% | mixed |
| 6.RP.A.3b | Solve Unit Rate Problems | 146 | 94,527 | 68 / 5 / 9 / 1 / 0 / 63 | REP 47% | PF 75% | mixed |
| 6.RP.A.3c | Solve Problems Involving Percents | 147 | 78,188 | 55 / 0 / 10 / 1 / 0 / 81 | PF 55% | PF 71% | mixed |
| 6.RP.A.3d | Use Ratios to Convert Measurement Units | 30 | 17,532 | 11 / 0 / 2 / 0 / 0 / 17 | PF 57% | PF 73% | mixed |
| 6.SP.A.1 | Recognize Statistical Questions Account for Variablility | 9 | 1,922 | 1 / 0 / 6 / 0 / 1 / 1 | J&P 67% | J&P 56% | mixed |
| 6.SP.A.2 | Understand Properties of Distribution with (or for) Data | 5 | 1,425 | 2 / 0 / 1 / 0 / 0 / 2 | REP 40% | J&P 40% | mixed |
| 6.SP.A.3 | Recognize Properties of Measure of Center with Variation | 7 | 811 | 0 / 1 / 3 / 0 / 0 / 3 | J&P 43% | PF 71% | mixed |
| 6.SP.B.4 | Display Numerical Data Using Dot Plots, Histograms & Box Plots | 26 | 6,796 | 7 / 1 / 17 / 0 / 0 / 1 | J&P 65% | J&P 62% | mostly J&P |
| 6.SP.B.5a | Report the Number of Observations in a Data Set | 1 | 0 | 1 / 0 / 0 / 0 / 0 / 0 | REP 100% | REP 100% | too few problems |
| 6.SP.B.5b | Describe the Attributes of a Data Set | 7 | 1,984 | 2 / 0 / 5 / 0 / 0 / 0 | J&P 71% | REP 57% | mixed |
| 6.SP.B.5c | Give & Describe Quantitative Measures of Center & Variability | 62 | 11,818 | 5 / 6 / 27 / 0 / 0 / 24 | J&P 44% | PF 52% | mixed |
| 6.SP.B.5d | Relate Measures of Center & Variablity to Distribution of Data | 4 | 221 | 0 / 0 / 4 / 0 / 0 / 0 | J&P 100% | J&P 75% | mostly J&P |
| 7.EE.A.1 | Apply Properties of Operations to Create Equivalent Expressions | 24 | 16,756 | 1 / 1 / 7 / 0 / 0 / 15 | PF 63% | PF 71% | mostly PF |
| 7.EE.A.2 | Understand Equivalent Expressions in Context | 13 | 11,367 | 7 / 0 / 3 / 0 / 0 / 3 | REP 54% | REP 54% | mixed |
| 7.EE.B.3 | Solve Applied Problems Using Numerical and Algebraic Expressions and Equations | 25 | 3,621 | 14 / 2 / 1 / 0 / 0 / 8 | REP 56% | PF 56% | mixed |
| 7.EE.B.4a | Solve 2-Step Equations | 107 | 80,067 | 28 / 1 / 12 / 1 / 0 / 65 | PF 61% | PF 70% | mostly PF |
| 7.EE.B.4b | Solve, Graph & Interpret 2-Step Inequalities | 28 | 19,232 | 2 / 0 / 13 / 0 / 0 / 13 | J&P 46% | PF 54% | mixed |
| 7.G.A.1 | Solve Scale Drawing Problems | 113 | 87,120 | 20 / 33 / 22 / 1 / 0 / 37 | PF 33% | PF 40% | mixed |
| 7.G.A.2 | Draw Geometric Shapes & Unique Triangles | 25 | 10,653 | 4 / 2 / 18 / 0 / 0 / 1 | J&P 72% | J&P 72% | mostly J&P |
| 7.G.A.3 | Describe 2D Cross Sections of 3D figures | 8 | 1,709 | 1 / 2 / 2 / 0 / 0 / 3 | PF 38% | PF 50% | mixed |
| 7.G.B.4 | Solve Problems Involving Area & Circumference of Circles | 105 | 83,004 | 39 / 5 / 16 / 1 / 0 / 44 | PF 42% | PF 59% | mixed |
| 7.G.B.5 | Use Facts About Angles to Write & Solve Equations | 44 | 26,337 | 10 / 1 / 19 / 0 / 0 / 14 | J&P 43% | J&P 48% | mixed |
| 7.G.B.6 | Find Area, Volume & Surface Area of 2D/3D Objects | 64 | 34,048 | 16 / 5 / 9 / 0 / 0 / 34 | PF 53% | PF 61% | mixed |
| 7.NS.A.1a | Describe Situations Where Opposite Quantities Combine to Make 0 | 1 | 33 | 0 / 1 / 0 / 0 / 0 / 0 | A&G 100% | A&G 100% | too few problems |
| 7.NS.A.1b | Interpret Sums of Rational Numbers | 10 | 7,490 | 4 / 0 / 4 / 0 / 0 / 2 | REP 40% | REP 50% | mixed |
| 7.NS.A.1c | Understand Properties of Subtracting Rational Numbers | 9 | 4,471 | 1 / 1 / 3 / 0 / 0 / 4 | PF 44% | PF 56% | mixed |
| 7.NS.A.1d | Apply Properties of Operations to Add/Subtract Rational Numbers | 41 | 37,450 | 7 / 2 / 0 / 0 / 0 / 32 | PF 78% | PF 98% | mostly PF |
| 7.NS.A.2a | Understand Applied Context for Multiplying Rational Numbers | 6 | 3,671 | 2 / 0 / 0 / 0 / 0 / 4 | PF 67% | PF 100% | mostly PF |
| 7.NS.A.2b | Understand Applied Context for Dividing Rational Numbers | 9 | 970 | 1 / 2 / 0 / 0 / 0 / 6 | PF 67% | PF 56% | mixed |
| 7.NS.A.2c | Apply Properties of Operations to Multiply/Divide Rational Numbers | 47 | 49,156 | 3 / 1 / 1 / 0 / 0 / 42 | PF 89% | PF 94% | one practice (PF) |
| 7.NS.A.2d | Convert a Rational Number to a Decimal | 10 | 3,864 | 0 / 0 / 1 / 0 / 0 / 9 | PF 90% | PF 70% | mostly PF |
| 7.NS.A.3 | Solve Applied Problems Involving All Operations of Rational Numbers | 8 | 1,817 | 1 / 0 / 0 / 0 / 0 / 7 | PF 88% | PF 100% | one practice (PF) |
| 7.RP.A.1 | Compute Unit Rates with Fractions | 16 | 15,794 | 4 / 0 / 2 / 0 / 0 / 10 | PF 63% | PF 94% | mostly PF |
| 7.RP.A.2a | Identify Proportional Relationships | 111 | 67,238 | 32 / 18 / 26 / 1 / 0 / 34 | PF 31% | PF 42% | mixed |
| 7.RP.A.2b | Identify the Constant of Proportionality | 24 | 26,998 | 3 / 5 / 7 / 0 / 0 / 9 | PF 38% | PF 38% | mixed |
| 7.RP.A.2c | Represent Proportional Relationships with Equations | 56 | 54,757 | 23 / 6 / 7 / 0 / 0 / 20 | REP 41% | REP 39% | mixed |
| 7.RP.A.2d | Interpret Points on Proportional Graphs | 7 | 653 | 1 / 0 / 4 / 0 / 0 / 2 | J&P 57% | J&P 43% | mixed |
| 7.RP.A.3 | Use Proportional Relationships to Solve Ratio & Percent Problems | 198 | 127,884 | 86 / 11 / 13 / 0 / 0 / 88 | PF 44% | PF 55% | mixed |
| 7.SP.A.1 | Interpret Methods of Sampling | 11 | 2,274 | 0 / 1 / 10 / 0 / 0 / 0 | J&P 91% | J&P 82% | one practice (J&P) |
| 7.SP.A.2 | Use Random Samples to Draw Influences | 22 | 2,191 | 4 / 3 / 11 / 1 / 0 / 3 | J&P 50% | J&P 50% | mixed |
| 7.SP.B.3 | Compare Populations using Center & Variability | 12 | 1,533 | 1 / 1 / 7 / 0 / 0 / 3 | J&P 58% | J&P 67% | mixed |
| 7.SP.B.4 | Draw Inferences using Measures of Center & Variability | 27 | 3,186 | 2 / 2 / 16 / 1 / 0 / 6 | J&P 59% | J&P 59% | mixed |
| 7.SP.C.5 | Understand that Probability is Between 0-1 & Describes the Likelihood of an Event Occurring | 20 | 3,762 | 6 / 2 / 12 / 0 / 0 / 0 | J&P 60% | J&P 75% | mostly J&P |
| 7.SP.C.6 | Approximate Probability of an Event by Collecting Data | 10 | 2,800 | 3 / 1 / 2 / 0 / 0 / 4 | PF 40% | J&P 40% | mixed |
| 7.SP.C.7a | Develop a Uniform Probabilty Model of a Single Event | 8 | 2,262 | 3 / 2 / 3 / 0 / 0 / 0 | REP 38% | REP 38% | mixed |
| 7.SP.C.7b | Develop a Probability Model of a Single Event | 5 | 2,032 | 1 / 2 / 2 / 0 / 0 / 0 | A&G 40% | REP 60% | mixed |
| 7.SP.C.8a | Understand Probability of a Compound Event | 8 | 1,830 | 3 / 2 / 1 / 0 / 0 / 2 | REP 38% | REP 63% | mixed |
| 7.SP.C.8b | Represent Sample Spaces for Compound Events | 21 | 7,378 | 8 / 6 / 1 / 0 / 0 / 6 | REP 38% | REP 33% | mixed |
| 7.SP.C.8c | Design & Use a Simulation for Compound Events | 7 | 2,330 | 3 / 0 / 3 / 0 / 0 / 1 | REP 43% | REP 43% | mixed |
| 8.EE.A.1 | Know & Apply Properties of Exponents | 29 | 8,989 | 3 / 6 / 2 / 0 / 0 / 18 | PF 62% | PF 76% | mostly PF |
| 8.EE.A.2 | Evaluate Square & Cube Roots | 33 | 11,401 | 2 / 2 / 2 / 0 / 0 / 27 | PF 82% | PF 79% | mostly PF |
| 8.EE.A.3 | Expressing Quantities in Scientific Notation | 15 | 4,190 | 3 / 4 / 4 / 0 / 0 / 4 | A&G 27% | PF 33% | mixed |
| 8.EE.A.4 | Apply Scientific Notation Operations | 31 | 2,096 | 4 / 2 / 10 / 1 / 0 / 14 | PF 45% | PF 55% | mixed |
| 8.EE.B.5 | Compare Slopes of Proportional Relationships | 11 | 1,519 | 2 / 1 / 5 / 0 / 0 / 3 | J&P 45% | PF 45% | mixed |
| 8.EE.B.6 | Find Slope of a Line using Similar Triangles | 25 | 8,603 | 2 / 5 / 5 / 0 / 0 / 13 | PF 52% | PF 52% | mixed |
| 8.EE.C.7a | Solve Linear Equations with One, Multiple or No Solutions | 20 | 8,962 | 1 / 0 / 15 / 0 / 0 / 4 | J&P 75% | J&P 55% | mixed |
| 8.EE.C.7b | Solve Multi-Step Linear Equations with Rational Number Coefficients | 60 | 32,405 | 6 / 1 / 7 / 0 / 0 / 46 | PF 77% | PF 85% | mostly PF |
| 8.EE.C.8a | Identify Solutions to Systems of Equations Using Graphs | 21 | 4,964 | 1 / 4 / 12 / 0 / 0 / 4 | J&P 57% | J&P 43% | mixed |
| 8.EE.C.8b | Solve Systems of Linear Equations Algebraically | 9 | 5,246 | 2 / 0 / 3 / 0 / 0 / 4 | PF 44% | PF 56% | mixed |
| 8.EE.C.8c | Solve Systems of Linear Equations Word Problems | 21 | 11,566 | 10 / 0 / 5 / 0 / 0 / 6 | REP 48% | REP 43% | mixed |
| 8.F.A.1 | Understand Definition of a Function | 14 | 5,559 | 0 / 1 / 6 / 0 / 0 / 7 | PF 50% | PF 50% | mixed |
| 8.F.A.2 | Compare Functions in Different Forms | 3 | 754 | 1 / 0 / 0 / 0 / 0 / 2 | PF 67% | REP 33% | mixed |
| 8.F.A.3 | Identify Linear & Non-Linear Functions | 11 | 2,101 | 1 / 2 / 5 / 0 / 0 / 3 | J&P 45% | PF 36% | mixed |
| 8.F.B.4 | Use Functions to Model Relationships Between Quantities | 57 | 22,351 | 15 / 6 / 15 / 0 / 0 / 21 | PF 37% | PF 44% | mixed |
| 8.F.B.5 | Qualitatively Describe & Graph Relationships | 22 | 4,343 | 12 / 2 / 7 / 0 / 0 / 1 | REP 55% | REP 59% | mixed |
| 8.G.A.1a | Apply Properties of Transformations to Lines & Line Segments | 10 | 1,041 | 0 / 0 / 10 / 0 / 0 / 0 | J&P 100% | J&P 90% | one practice (J&P) |
| 8.G.A.1b | Apply the Properties of Transformations to Angles | 24 | 6,088 | 1 / 2 / 17 / 0 / 0 / 4 | J&P 71% | J&P 50% | mixed |
| 8.G.A.1c | Apply the Properties of Transformations to Parallel Lines | 1 | 31 | 0 / 0 / 1 / 0 / 0 / 0 | J&P 100% | J&P 100% | too few problems |
| 8.G.A.2 | Understand & Describe Geometric Transformation Sequences | 21 | 3,457 | 0 / 0 / 21 / 0 / 0 / 0 | J&P 100% | J&P 86% | one practice (J&P) |
| 8.G.A.3 | Describe the Effect of Transformations on 2D Figures | 14 | 5,824 | 0 / 1 / 8 / 0 / 0 / 5 | J&P 57% | PF 43% | mixed |
| 8.G.A.4 | use Transformations to Determine Similarity in 2D figures | 18 | 6,512 | 7 / 1 / 9 / 0 / 0 / 1 | J&P 50% | J&P 50% | mixed |
| 8.G.A.5 | Use Informal Arguments to Establish Facts about Angles for Similar Triangles | 10 | 3,354 | 0 / 0 / 7 / 0 / 0 / 3 | J&P 70% | J&P 60% | mostly J&P |
| 8.G.B.6 | Prove the Pythagorean Theorem & it's Converse | 1 | 166 | 0 / 0 / 1 / 0 / 0 / 0 | J&P 100% | J&P 100% | too few problems |
| 8.G.B.7 | Apply the Pythagorean Theorem to 2D & 3D FIgures | 38 | 8,846 | 5 / 1 / 12 / 1 / 0 / 19 | PF 50% | PF 61% | mixed |
| 8.G.B.8 | Apply the Pythagorean Theorem to Find the Distance Between Points on the Coordinate Plane | 11 | 398 | 1 / 0 / 0 / 0 / 0 / 10 | PF 91% | PF 91% | one practice (PF) |
| 8.G.C.9 | Know & Use Volume Formulas | 92 | 23,400 | 13 / 15 / 7 / 1 / 0 / 56 | PF 61% | PF 72% | mostly PF |
| 8.NS.A.1 | Understand & Approximate Rational & Irrational Numbers | 9 | 739 | 1 / 0 / 3 / 0 / 0 / 5 | PF 56% | PF 67% | mixed |
| 8.NS.A.2 | Approximate Irrational Numbers | 28 | 10,227 | 6 / 0 / 3 / 0 / 0 / 19 | PF 68% | PF 82% | mostly PF |
| 8.SP.A.1 | Construct & Interpret Scatter Plots | 16 | 3,405 | 2 / 5 / 9 / 0 / 0 / 0 | J&P 56% | J&P 56% | mixed |
| 8.SP.A.2 | Determine Line of Best Fit for Scatter Plots | 11 | 1,520 | 1 / 1 / 6 / 0 / 0 / 3 | J&P 55% | J&P 36% | mixed |
| 8.SP.A.3 | Use Linear Equations Applied to Bivariate Data | 15 | 1,951 | 4 / 0 / 4 / 0 / 0 / 7 | PF 47% | PF 40% | mixed |
| 8.SP.A.4 | Construct & Interpret Two Way Tables | 7 | 612 | 0 / 0 / 7 / 0 / 0 / 0 | J&P 100% | J&P 100% | one practice (J&P) |
