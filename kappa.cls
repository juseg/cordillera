%% IDENTIFCATION
\NeedsTeXFormat{LaTeX2e}[1995/12/01]
\ProvidesClass{kappa}
\RequirePackage{graphicx}

%% DECLARE CLASS OPTIONS
\DeclareOption{letterpaper}{\setlength{\paperheight}{11in}
                            \setlength{\paperwidth}{8.5in}}
\DeclareOption{a4paper}{\setlength{\paperheight}{297mm}
                        \setlength{\paperwidth}{210mm}}
\DeclareOption{a5paper}{\OptionNotUsed}
\DeclareOption{b5paper}{\OptionNotUsed}
\DeclareOption{legalpaper}{\OptionNotUsed}
\DeclareOption{executivepaper}{\OptionNotUsed}
\DeclareOption{landscape}{\OptionNotUsed}
\DeclareOption{12pt}{\OptionNotUsed}
\DeclareOption{11pt}{\OptionNotUsed}
\DeclareOption{10pt}{\OptionNotUsed}
\DeclareOption{oneside}{\@twosidefalse \@mparswitchfalse}
\DeclareOption{twoside}{\@twosidetrue  \@mparswitchtrue}
\DeclareOption{onecolumn}{\@twocolumnfalse \@mparswitchfalse}
\DeclareOption{twocolumn}{\@twocolumntrue \@mparswitchtrue}

\newif\if@draft
\@draftfalse
\DeclareOption{draft}{\renewcommand{\baselinestretch}{1.7}\@drafttrue
                      \ExecuteOptions{oneside,onecolumn}}
\renewcommand{\baselinestretch}{1}              % Default single line spacing
\ExecuteOptions{oneside,twocolumn}      % Process defaults
\ProcessOptions                                 % Execute class options if supplied

%% NEW MACROS AND CONSTANTS
\newcommand{\@pagenumprefix}{}                                   % Page number prefix
\newcommand{\partname}{Part}                                     %
\newcommand{\appendixname}{Appendix}                             % Name of Appendix header
\newcommand{\contentsname}{Contents}                             % Name of Contents header
\newcommand{\listfigurename}{List of Figures}                    % Name of List of figures header
\newcommand{\listtablename}{List of Tables}                      % Name of List of Tables header
\newcommand{\refname}{References}                                % Name of References header
\newcommand{\indexname}{Index}                                   % Name of index header
\newcommand{\figurename}{Figure}                                 % Name of Figure captions
\newcommand{\tablename}{Table}                                   % Name of Table captions
\newcommand{\@abstractheading}{{\normalsize\bfseries Abstract.}\ } % Name of Abstract header
\newcommand{\@keywordheading}{{\itshape Keywords: \ }}
\newcommand{\@acknowledgementheading}{{\normalsize\bfseries Acknowledgements.}\ } % Name of Acknowledgement header

\newcommand{\@titlestyle}{\Large\bfseries}                       % Format on Title
\newcommand{\@authorstyle}{\large}                               % Format on Author list
\newcommand{\@historystyle}{\small}                              % Format on paper history list
\newcommand{\@addressstyle}{\small\itshape}                      % Format on Address field
\newcommand{\@abstractstyle}{\normalfont\small}                  % Format on abstract
\newcommand{\@keywordstyle}{\normalfont\small}                   % Format on keywords
\newcommand{\@acknowledgestyle}{\normalfont\small}               % Format on acknowledgement
\newcommand{\@runheadstyle}{\normalsize}
\newcommand{\@foottextstyle}{\scriptsize}
\newcommand{\@headtextstyle}{\small}
\newcommand{\@pagenumberstyle}{\normalfont\normalsize}
\newcommand{\@captionstyle}{\normalfont\bfseries\small}

\def\@captionsize{\small}
\def\@tablecaptionsize{\@captionsize}
\def\@figurecaptionsize{\@captionsize}
\def\@tablesize{\footnotesize}
\def\@bibliosize{\small}

\newlength{\@aboveabstractskip}
\setlength{\@aboveabstractskip}{24\p@ \@plus 6\p@ \@minus 2\p@}
\newlength{\@abovekeywordskip}
\setlength{\@abovekeywordskip}{12\p@}
\newlength{\@abstractleftskip}
\setlength{\@abstractleftskip}{55\p@}                           % Space above upper frontmatter rule
\newlength{\@abstractrightskip}
\setlength{\@abstractrightskip}{55\p@}                          % Space above upper frontmatter rule
\newlength{\@belowfmskip}
\setlength{\@belowfmskip}{24\p@ \@plus 6\p@ \@minus 2\p@}

% CAPTION
\newlength\abovecaptionskip
\setlength\abovecaptionskip{12\p@}
\newlength\belowcaptionskip
\setlength\belowcaptionskip{0\p@}
\newlength\@figureindent
\setlength\@figureindent{25\p@}

%% FLOAT PLACEMENT FRACTION
\setcounter{topnumber}{5}
\renewcommand\topfraction{.99}
\setcounter{bottomnumber}{5}
\renewcommand\bottomfraction{.99}
\setcounter{totalnumber}{10}
\renewcommand\textfraction{.05}
\renewcommand\floatpagefraction{.9}
\setcounter{dbltopnumber}{5}
\renewcommand\dbltopfraction{.99}
\renewcommand\dblfloatpagefraction{.8}

\setlength\floatsep    {12\p@ \@plus 2\p@ \@minus 2\p@}
\setlength\textfloatsep{24\p@ \@plus 2\p@ \@minus 4\p@}
\setlength\intextsep   {12\p@ \@plus 2\p@ \@minus 2\p@}
\setlength\dblfloatsep    {12\p@ \@plus 2\p@ \@minus 2\p@}
\setlength\dbltextfloatsep{24\p@ \@plus 2\p@ \@minus 4\p@}
\setlength\@fptop{0\p@ \@plus 1fil}
\setlength\@fpsep{4\p@ \@plus 2fil}
\setlength\@fpbot{0\p@ \@plus 1fil}
\setlength\@dblfptop{0\p@ \@plus 1fil}
\setlength\@dblfpsep{4\p@ \@plus 2fil}
\setlength\@dblfpbot{0\p@ \@plus 1fil}

%% DEFINE FONT SIZE
\if@draft
    \renewcommand\normalsize{%
        \@setfontsize\normalsize\@xiipt{14.5}%
        \abovedisplayskip 12\p@ \@plus3\p@ \@minus7\p@
        \abovedisplayshortskip \z@ \@plus3\p@
        \belowdisplayshortskip 6.5\p@ \@plus3.5\p@ \@minus3\p@
        \belowdisplayskip \abovedisplayskip}

        \newcommand\small{%
            \@setfontsize\small\@xipt{13.6}%
            \abovedisplayskip 11\p@ \@plus3\p@ \@minus6\p@
            \abovedisplayshortskip \z@ \@plus3\p@
            \belowdisplayshortskip 6.5\p@ \@plus3.5\p@ \@minus3\p@
            \def\@listi{\leftmargin\leftmargini
                    \topsep 9\p@ \@plus3\p@ \@minus5\p@
                    \parsep 4.5\p@ \@plus2\p@ \@minus\p@
                    \itemsep \parsep}%
            \belowdisplayskip \abovedisplayskip}

        \newcommand\footnotesize{%
            \@setfontsize\footnotesize\@xpt\@xiipt
            \abovedisplayskip 10\p@ \@plus2\p@ \@minus5\p@
            \abovedisplayshortskip \z@ \@plus3\p@
            \belowdisplayshortskip 6\p@ \@plus3\p@ \@minus3\p@
            \def\@listi{\leftmargin\leftmargini
                \topsep 6\p@ \@plus2\p@ \@minus2\p@
                \parsep 3\p@ \@plus2\p@ \@minus\p@
                \itemsep \parsep}%
            \belowdisplayskip \abovedisplayskip}

    \newcommand\scriptsize{\@setfontsize\scriptsize\@viiipt{9.5}}
    \newcommand\tiny{\@setfontsize\tiny\@vipt\@viipt}
    \newcommand\large{\@setfontsize\large\@xivpt{18}}
    \newcommand\Large{\@setfontsize\Large\@xviipt{22}}
    \newcommand\LARGE{\@setfontsize\LARGE\@xxpt{25}}
    \newcommand\huge{\@setfontsize\huge\@xxvpt{30}}
    \let\Huge=\huge
\else
    \renewcommand\normalsize{%
        \@setfontsize\normalsize\@xpt\@xiipt
        \baselineskip 12\p@ % plus .001\p@ minus 0.25\p@           % Allow little stretch of the baseline
        \abovedisplayskip 12\p@ \@plus2\p@ \@minus5\p@
        \abovedisplayshortskip \z@ \@plus3\p@
        \belowdisplayshortskip 6\p@ \@plus3\p@ \@minus3\p@
        \belowdisplayskip \abovedisplayskip}

    \newcommand\small{%
        \@setfontsize\small\@ixpt{11}%
        \abovedisplayskip 8.5\p@ \@plus3\p@ \@minus4\p@
        \abovedisplayshortskip \z@ \@plus2\p@
        \belowdisplayshortskip 4\p@ \@plus2\p@ \@minus2\p@
        \def\@listi{\leftmargin\leftmargini
            \topsep 4\p@ \@plus2\p@ \@minus2\p@
            \parsep 2\p@ \@plus\p@ \@minus\p@
            \itemsep \parsep}%
        \belowdisplayskip \abovedisplayskip}

    \newcommand\footnotesize{%
        \@setfontsize\footnotesize\@viiipt{9.5}%
        \abovedisplayskip 6\p@ \@plus2\p@ \@minus4\p@
        \abovedisplayshortskip \z@ \@plus\p@
        \belowdisplayshortskip 3\p@ \@plus\p@ \@minus2\p@
        \def\@listi{\leftmargin\leftmargini
            \topsep 3\p@ \@plus\p@ \@minus\p@
            \parsep 2\p@ \@plus\p@ \@minus\p@
            \itemsep \parsep}%
        \belowdisplayskip \abovedisplayskip}

        \newcommand\scriptsize{\@setfontsize\scriptsize\@viipt\@viiipt}
        \newcommand\tiny{\@setfontsize\tiny\@vpt\@vipt}
        \newcommand\large{\@setfontsize\large\@xiipt{14}}
        \newcommand\Large{\@setfontsize\Large\@xivpt{18}}
        \newcommand\LARGE{\@setfontsize\LARGE\@xviipt{22}}
        \newcommand\huge{\@setfontsize\huge\@xxpt{25}}
        \newcommand\Huge{\@setfontsize\Huge\@xxvpt{30}}
\fi

% DEFAULT: The normalsize font
\normalsize

%% DEFINE LATEX209 FONTS FAMILIES AND SHAPES
\DeclareOldFontCommand{\rm}{\normalfont\rmfamily}{\mathrm}
\DeclareOldFontCommand{\sf}{\normalfont\sffamily}{\mathsf}
\DeclareOldFontCommand{\tt}{\normalfont\ttfamily}{\mathtt}
\DeclareOldFontCommand{\bf}{\normalfont\bfseries}{\mathbf}
\DeclareOldFontCommand{\it}{\normalfont\itshape}{\mathit}
\DeclareOldFontCommand{\sl}{\normalfont\slshape}{\@nomath\sl}
\DeclareOldFontCommand{\sc}{\normalfont\scshape}{\@nomath\sc}
\DeclareRobustCommand*\cal{\@fontswitch\relax\mathcal}
\DeclareRobustCommand*\mit{\@fontswitch\relax\mathnormal}

%% DEFINE PAPERSIZE ,MARGINS AND COLUMNSEPARTATION FOR ONE AND TWO SIDED TEXT
\setlength{\lineskip}{0\p@}
\setlength{\normallineskip}{1\p@}
\frenchspacing

\if@twoside                                     % Values for two-sided printing:
    \newcommand{\@frontmatterwidth}{1\textwidth}% Default is text width
    \setlength{\oddsidemargin}{44\p@}           %   Left margin on odd-numbered pages
    \setlength{\evensidemargin}{82\p@}          %   Left margin on even-numbered pages
    \setlength\textwidth{345\p@}                %   Text width
    \setlength{\marginparwidth}{107\p@}         %   Width of marginal notes
    \if@twocolumn                               % Values for two-column mode:
        \setlength{\oddsidemargin}{0mm}         %   Left margin on odd-numbered pages
        \setlength{\textwidth}{160mm}           %   Width of text body
        \setlength{\columnsep}{22\p@}           %   Space between columns - used 16 before
        \setlength{\columnseprule}{\z@}         %   Width of rule between columns
        \addtolength{\textwidth}{\columnsep}    %   Adding to width of text body
        \renewcommand{\@frontmatterwidth}{1\textwidth} % Default is text width
        \setlength{\marginparwidth}{42\p@}      %   Width of marginal notes
        \let\@tempdimb\paperwidth               % Calculates the left margin on even-numbered pages
        \addtolength{\@tempdima}{2in}
        \addtolength{\@tempdima}{\hoffset}
        \addtolength{\@tempdima}{\oddsidemargin}
        \addtolength{\@tempdima}{\textwidth}
        \addtolength{\@tempdimb}{-\@tempdima}
        \setlength{\evensidemargin}{\@tempdimb} %   Left margin on even-numbered pages
    \fi
\else                                           % Values for one-sided printing:
    \newcommand{\@frontmatterwidth}{1\textwidth}% Default is text width
    \setlength{\evensidemargin}{63\p@}          %   Left margin on even-numbered pages.
    \setlength{\oddsidemargin}{63\p@}           %   Left margin on odd-numbered pages.
    \setlength{\marginparwidth}{90\p@}          %   Width of marginal notes
    \setlength\textwidth{345\p@}                %   Text width
    \if@twocolumn                               % Values for two-column mode:
        \setlength{\evensidemargin}{-2.4mm}     %   Left margin on even-numbered pages.
        \setlength{\oddsidemargin}{-2.4mm}      %   Left margin on odd-numbered pages.
        \setlength{\textwidth}{160mm}           %   Width of text body
        \setlength{\columnsep}{11\p@}           %   Space between columns
        \setlength{\columnseprule}{\z@}         %   Width of rule between columns
        \addtolength{\textwidth}{\columnsep}    %   Adding to width of text body
        \renewcommand{\@frontmatterwidth}{1\textwidth} % Default is text width
        \setlength{\marginparwidth}{42\p@}      %   Width of marginal notes
    \fi
\fi

\setlength{\topmargin}{-6\p@}                     % Nominal distance from top of page to top of box containing running head

\if@twocolumn
    \@tempdima=651pt \advance\@tempdima -\topskip \@tempcnta=\@tempdima
    \@tempdimb=\baselinestretch\baselineskip \@tempcntb=\@tempdimb
    \divide\@tempcnta\@tempcntb
    \setlength{\textheight}{\baselinestretch\baselineskip}
    \multiply\textheight\@tempcnta
    \addtolength{\textheight}{\topskip}
\else
    \@tempdima=651pt \advance\@tempdima -\topskip \@tempcnta=\@tempdima
    \@tempdimb=\baselinestretch\baselineskip \@tempcntb=\@tempdimb
    \divide\@tempcnta\@tempcntb
    \setlength{\textheight}{\baselinestretch\baselineskip}
    \multiply\textheight\@tempcnta
    \addtolength{\textheight}{\topskip}
\fi

\setlength{\headheight}{\baselineskip}          % Height of box containing running head
\setlength{\headsep}{18\p@}                     % Space between running head and text
\setlength{\topskip}{\z@}%\baselineskip}             % distance from top body to bottom of first line of text
\setlength{\footskip}{30\p@}                    % Space between running foot and text
\setlength\maxdepth{.5\topskip}                 %
\setlength{\parskip}{0\p@}%                     % Extra vertical space between paragraphs

\if@twocolumn                                   % Indentation of each paragraph and maginal notes
  \setlength\parindent{1.5em}
  \setlength{\marginparsep}{7\p@}               % Horizontal space between outer and marginal note
  \setlength{\marginparpush}{5\p@}              % Minimum vertical separation between two marginalnotes
\else
  \setlength\parindent{15\p@}
  \setlength{\marginparsep}{7\p@}               % Horizontal space between outer and marginal note
  \setlength{\marginparpush}{5\p@}              % Minimum vertical separation between two marginalnotes
\fi

\setlength\smallskipamount{3\p@ \@plus 1\p@ \@minus 1\p@}
\setlength\medskipamount{6\p@ \@plus 2\p@ \@minus 2\p@}
\setlength\bigskipamount{12\p@ \@plus 4\p@ \@minus 4\p@}

\setlength{\footnotesep}{8.4\p@}
\setlength{\skip\footins}{12\p@ \@plus 8\p@}   % Space between last line of text and top of first footnote


%% PENALTIES
\@lowpenalty   51                   % Produced by \nopagebreak[1] or \nolinebreak[1]
\@medpenalty  151                   % Produced by \nopagebreak[2] or \nolinebreak[2]
\@highpenalty 301                   % Produced by \nopagebreak[3] or \nolinebreak[3]
\@beginparpenalty -\@lowpenalty     % Before a list or paragraph environment
\@endparpenalty   -\@lowpenalty     % After a list or paragraph environment
\@itempenalty     -\@lowpenalty     % Between list items

\clubpenalty=10000                  % Penalty for leaving a single line on bottom of page
\widowpenalty=10000                 % Penalty for single line on top of page
\displaywidowpenalty=50             % Penalty for math displays on top of page
\predisplaypenalty=10000            % Penalty for breaking before math display
\postdisplaypenalty=100             % Penalty for breaking after math display
\interlinepenalty=0                 % Allow breaking in middle of paragraph
\brokenpenalty=100                  % Allow breaking of a page after a hyphenated line

\if@twocolumn
  \flushbottom
  \sloppy
\fi

\if@twoside
\else
  \raggedbottom
\fi

%% DEFINES SECTIONS
\newcounter{part}
\newcounter{section}
\newcounter{subsection}[section]
\newcounter{subsubsection}[subsection]
\newcounter{paragraph}[subsubsection]
\newcounter{subparagraph}[paragraph]
\setcounter{secnumdepth}{4}

%% FORMAT ON SECTION NUMBERING
\renewcommand \thepart {\@Roman\c@part}
\renewcommand \thesection {\@arabic\c@section.}
\renewcommand \thesubsection   {\thesection\@arabic\c@subsection.}
\renewcommand \thesubsubsection{\thesubsection\@arabic\c@subsubsection.}
\renewcommand \theparagraph    {\thesubsubsection\@arabic\c@paragraph.}
\renewcommand \thesubparagraph {\theparagraph\@arabic\c@subparagraph.}

\newcommand\part{%
   \if@noskipsec \leavevmode \fi
   \par
   \addvspace{4ex}%
   \@afterindentfalse
   \secdef\@part\@spart}
\def\@part[#1]#2{%
    \ifnum \c@secnumdepth >\m@ne
      \refstepcounter{part}%
      \addcontentsline{toc}{part}{\thepart\hspace{1em}#1}%
    \else
      \addcontentsline{toc}{part}{#1}%
    \fi
    {\parindent \z@ \raggedright
     \interlinepenalty \@M
     \normalfont
     \ifnum \c@secnumdepth >\m@ne
       \Large\bfseries \partname\nobreakspace\thepart
       \par\nobreak
     \fi
     \huge \bfseries #2%
     \markboth{}{}\par}%
    \nobreak
    \vskip 3ex
    \@afterheading}
\def\@spart#1{%
    {\parindent \z@ \raggedright
     \interlinepenalty \@M
     \normalfont
     \huge \bfseries #1\par}%
     \nobreak
     \vskip 3ex
     \@afterheading}

\def\section{\@startsection{section}{1}{\z@}%
                                    {-1.5\baselineskip \@plus 0.3\baselineskip \@minus 0.1\baselineskip}%
                                    {1\baselineskip}
                                    {\raggedright\large\bfseries\hyphenpenalty\@M}}
\def\subsection{\@startsection{subsection}{2}{\z@}%
                                    {-1\baselineskip \@plus 0.3\baselineskip \@minus 0.1\baselineskip}
                                    {0.4\baselineskip}
                                    {\raggedright\normalsize\bfseries\hyphenpenalty\@M}}
\def\subsubsection{\@startsection{subsubsection}{3}{\z@}%
                                    {-1\baselineskip \@plus .3\baselineskip \@minus 0.1\baselineskip}
                                    {1\p@}
                                    {\raggedright\normalsize\itshape\hyphenpenalty\@M}}
\def\paragraph{\@startsection{paragraph}{4}{\z@}%
                                    {0.5\baselineskip \@plus .1\baselineskip \@minus .1\baselineskip}
                                    {-1em}
                                    {\normalfont\normalsize\MakeUppercase}}

%% PAGE FOOT AND HEAD NUMBERING
\newif\if@usr@runauthor
\@usr@runauthorfalse
\newif\if@usr@runtitle
\@usr@runtitlefalse
\usepackage[utf8]{inputenc}

\pagenumbering{arabic}                                                % Arabic page numbers
\renewcommand{\thepage}{\@pagenumprefix\arabic{page}}                 % Add any prefix to page number
\newcommand{\runningauthor}[1]{\gdef\@runauthor{\uppercase{#1}}%      % Running author
            \@usr@runauthortrue}
\newcommand{\runauthor@text}{%
             \@ifundefined{@runauthor}{\global\def\@runauthor{}}{}}
\newcommand{\runningtitle}[1]{\gdef\@runtitle{\uppercase{#1}}%        % Running title
            \@usr@runtitletrue}
\newcommand{\runtitle@text}{%
             \@ifundefined{@runtitle}{\global\def\@runtitle{}}{}}

\if@twoside
        \renewcommand{\@oddfoot}{\hfil\@pagenumberstyle\thepage}
        \renewcommand{\@evenfoot}{\@pagenumberstyle\thepage\hfil}
        \renewcommand{\@evenhead}{\hfil\@headtextstyle\runauthor@text{\@runauthor}\hfil}
        \renewcommand{\@oddhead}{\hfil\@headtextstyle\runtitle@text{\@runtitle}\hfil}
\else
        \renewcommand{\@oddfoot}{\hfil\@pagenumberstyle\thepage\hfil}
        \let\@evenfoot\@oddfoot
        \renewcommand{\@evenhead}{\hfil\@headtextstyle\MakeUppercase{\@runauthor}\hfil}
        \renewcommand{\@oddhead}{\hfil\@headtextstyle\MakeUppercase{\@runtitle}\hfil}
\fi

\newcounter{firstpage}
\setcounter{firstpage}{1}
\newcounter{lastpage}
\setcounter{lastpage}{0}
\newcommand{\firstpage}[1]{\newcommand{\@tempa}{#1}
            \ifx\@tempa\@empty
            \else
                \setcounter{firstpage}{#1}
                \global\c@page=#1
                \ignorespaces
            \fi}
\newcommand{\lastpage}[1]{\newcommand{\@tempa}{#1}
            \ifx\@tempa\@empty
            \else
                \setcounter{lastpage}{#1}
                \ignorespaces
            \fi}

%% PREAMBLE COMMANDS FOR FRONTPAGE AND COPYRIGHT PAGES
\newcommand{\candidate}[1]{\newcommand{\@candidate}{#1}}
\newcommand{\thesistitle}[1]{\newcommand{\@thesistitle}{#1}}
\newcommand{\pubyear}[1]{\newcommand{\@pubyear}{#1}}
\newcommand{\department}[1]{\newcommand{\@department}{#1}}
\newcommand{\university}[1]{\newcommand{\@university}{#1}}
\newcommand{\issn}[1]{\newcommand{\@issn}{#1}}
\newcommand{\isbn}[1]{\newcommand{\@isbn}{#1}}
\newcommand{\layout}[1]{\newcommand{\@layout}{#1}}
\newcommand{\printed}[1]{\newcommand{\@printed}{#1}}
\newcommand{\coverpic}[1]{\newcommand{\@coverpic}{#1}}

%% FORMAT OF
\newcommand{\thesistitle@fmt}{\bfseries\huge}
\newcommand{\candidate@fmt}{\Large\textrm}
\newcommand{\pubyear@fmt}{\large\textrm}
\newcommand{\department@fmt}{\large\textrm}
\newcommand{\university@fmt}{\large\textrm}
\newcommand{\copyright@fmt}{\normalsize}

\newif\if@restonecol

% FRONTPAGE PAGE
\newcommand{\frontpage}{
           \if@twocolumn                                % Temporary switches of two-column mode
             \@restonecoltrue\onecolumn
           \else
             \@restonecolfalse
           \fi
           \@frontpage@fmt                              % Creates and formats box
           \unvbox\fp@box                               % Print box on page
           \if@restonecol                               % Restores two-column mode
               \twocolumn
               \newpage
           \else
             \newpage
           \fi
             }

\newbox{\fp@box}                                        % Initalize frontpage box
\newcommand{\@frontpage@fmt}{
            \clearpage                                  % Make sure there is a new page and odd page
            \if@twoside
                \ifodd
                    \c@page\thispagestyle{empty}
                \else
                    \hbox{}
                    \newpage\thispagestyle{empty}
                \fi
            \fi
            \global\setbox\fp@box=\vbox{                % Creates box
            \hyphenpenalty\@M                           % Not hyphenated
            \setlength{\parindent}{\z@}                 % No indent on paragraphs
            \setlength{\parskip}{\z@}                   % Paragraph skip
            \centering
            \vspace*{\stretch{1}}                       % Stretches out vspace so that title is 1/3 from tops
            \@ifundefined{@thesistitle}
                {}{\vbox{\thesistitle@fmt\@thesistitle}}\par
            \normalsize\vspace{5\baselineskip}          % 2 baselines between title and author
            \@ifundefined{@candidate}
                {}{\vbox{\candidate@fmt\@candidate}}\par
            \vspace*{\stretch{4}}                       % Stretches out vspace so that title is 1/3 from top
            \hfill\vbox{\includegraphics[height=20mm]{SUlogo.pdf}}\hfill\par
            \normalsize\vspace*{2\baselineskip}          %
            \@ifundefined{@department}
                    {\department@fmt Department of Physical Geography and Quaternary Geology}
                    {\department@fmt\@department}\par
            \@ifundefined{@university}
                    {\university@fmt Stockholm University}
                    {\university@fmt\@university}\par
            \textrm{\large Stockholm}\space
            \@ifundefined{@pubyear}
                    {\the\year}
                    {\pubyear@fmt\@pubyear}}}


\newcommand{\copyrightpage}{
           \if@twocolumn                                % Temporary switches of two-column mode
             \@restonecoltrue\onecolumn
           \else
             \@restonecolfalse
           \fi
           \@copyrightpage@fmt                          % Creates and formats box
           \unvbox\cp@box                               % Print box on page
           \if@restonecol                               % Restores two-column mode
               \twocolumn
               \newpage
           \else
             \newpage
           \fi}

\newbox{\cp@box}
\newcommand{\@copyrightpage@fmt}{
            \thispagestyle{empty}
            \global\setbox\cp@box=\vbox{%                % Creates box
            \hyphenpenalty\@M                           % Not hyphenated
            \setlength{\parindent}{\z@}                 % No indent on paragraphs
            \setlength{\parskip}{\z@}                   % Paragraph skip
            \raggedright
            \vspace*{\stretch{1}}                       % Stretches out vspace so that title is 1/3 from tops
            \@ifundefined{@candidate}
                    {}{\copyright@fmt$\copyright$~\@candidate}\par
            \@ifundefined{@issn}
                    {}{\copyright@fmt ISSN:~\@issn}\par
            \@ifundefined{@isbn}
                    {}{\copyright@fmt ISBN:~\@isbn}\par
            \@ifundefined{@coverpic}
                    {}{\copyright@fmt Cover:~\@coverpic}\par
            \@ifundefined{@layout}
                    {}{\copyright@fmt Layout:~\@layout}\par
            \@ifundefined{@printed}
                    {}{\copyright@fmt Printed by~\@printed}\par
            }}

%% FORNTMATTER
\newcount\sv@hyphenpenalty                    % Count register to save \hyphenpenalty
\newif\if@restonecol

\newenvironment{frontmatter}{
    \if@twocolumn                                % Temporary switches of two-column mode
        \@restonecoltrue\onecolumn
    \else
        \@restonecolfalse
    \fi
    \thispagestyle{empty}
    }
{%
    \@frontpage@fmt                              % Creates and formats box
    \unvbox\fp@box                               % Print box on page
    \newpage
    \@copyrightpage@fmt                          % Creates and formats box
    \unvbox\cp@box                               % Print box on page
    \newpage
    \thispagestyle{empty}
    \if@hasabstract                              % IF abstract/ keywords THEN
        {\noindent Doctoral dissertation~\@pubyear\par}
        {\noindent \@candidate\par}
        {\noindent \@department\par}
        {\noindent \@university\par}
        \vspace*{\stretch{1}}
        \vspace{\@aboveabstractskip}
        \unvbox\t@abstract                    % Appends abstract box
        \if@haskeywords                           % IF keywords exist print them
            \vspace{\@abovekeywordskip}           % Space over keyword list
            \unvbox\t@keyword                     % Appends keywords box
        \fi
        \vspace*{\stretch{3}}
    \fi
    \vspace{\@belowfmskip}                    % Vertical space below frontmatter
    \cleardoublepage
    \thispagestyle{empty}
    \if@hasthepapers                          % IF papers exist print them
        {\parindent\z@
        \let\@tempdima\textwidth
        \addtolength{\@tempdima}{-\@abstractleftskip}
        \addtolength{\@tempdima}{-\@abstractleftskip}
        \vspace*{\stretch{1}}
        \hspace*{\stretch{1}}
        \vbox{\hsize=\@tempdima\centering\Large\@thesistitle}
        \hspace*{\stretch{1}}
        \par
        \vspace{3\baselineskip}
        \hspace*{\stretch{1}}
        \vbox{\hsize=\@tempdima\centering\large\@candidate}
        \hspace*{\stretch{1}}
        \vspace{3\baselineskip}
        \unvbox\t@thepapers                   % Appends thepapers box
        \vspace*{\stretch{3}}}
    \fi
    \cleardoublepage
    \thispagestyle{plain}
    \if@restonecol                               % Restores two-column mode
        \twocolumn
            \newpage
    \else
            \newpage
    \fi
    \setcounter{page}{1}
}

%% ABSTRACT ENVIRONMENT
\newif\if@hasabstract                               % If abstract exists
\newbox\t@abstract                                  % Box for abstract
\newenvironment{abstract}{
    \global\@hasabstracttrue                        % Abstract is available
    \hyphenpenalty\sv@hyphenpenalty                 % restore \hyphenpenalty
    \global\setbox\t@abstract=\vbox\bgroup          % Initialize the box for abstract
    \leftskip\@abstractleftskip                     % Space between text and box edge
    \rightskip\@abstractrightskip                   % Space between text and box edge
    \parfillskip\@flushglue                         % Horisontal space on last line of paragraph
    \@abstractstyle                                 % Text size of the abstract
    \parskip\z@                                     % The space between paragraphs
    \noindent\@abstractheading                      % Paragraph indent in abstract and Caption for Abstract
    \ignorespaces}
{\par \egroup}                                      % END ABSTRACT ENVIRONMENT

%% KEYWORD ENVIRONMENT
\newif\if@haskeywords                               % If keyword exists
\newbox\t@keyword                                   % Box for keyword abstract
\newenvironment{keyword}{
    \global\@haskeywordstrue                        % Keyword list is available
    \hyphenpenalty\sv@hyphenpenalty                 % restore \hyphenpenalty
    \def\sep{\unskip, }                             % separator for multiple keywords
    \global\setbox\t@keyword=\vbox\bgroup           % Initalize the box for keywords
    \leftskip\z@
    \rightskip\z@
    \leftskip\@abstractleftskip                     % Space between text and box edge
    \rightskip\@abstractrightskip                   % Space between text and box edge
    \parfillskip\@flushglue                         % Horisontal space on last line of paragraph
    \@keywordstyle                                  % Font of the keywords
    \parskip\z@                                     % The space between paragraphs
    \noindent\@keywordheading                       % No indent and print keyword header
    \ignorespaces}
{\par \egroup}                                      % END KEYWORD ENVIRONMENT

%% THEPAPERS ENVIRONMENT
\newif\if@hasthepapers                              % If keyword exists
\newbox\t@thepapers                                 % Box for keyword abstract
\newenvironment{thepapers}{
    \global\@hasthepaperstrue                       % Papers list is available
    \hyphenpenalty\sv@hyphenpenalty                 % restore \hyphenpenalty
    \global\setbox\t@thepapers=\vbox\bgroup         % Initalize the box for keywords
    \leftskip\@abstractleftskip                     % Space between text and box edge
    \rightskip\@abstractrightskip                   % Space between text and box edge
    \parfillskip\@flushglue                         % Horisontal space on last line of paragraph
    \parskip\z@
    \parindent\z@                                   % The space between paragraphs
    \ignorespaces}
{\par\egroup}                                       % END THEPAPERS ENVIRONMENT


%% FOTNOTE COMMNAND
\def\footnote{\@ifnextchar[{\@xfootnote}%
        {\refstepcounter{\@mpfn}\protected@xdef\@thefnmark{\thempfn}\@footnotemark\@footnotetext}}%

% FORMAT OF FOOTNOTES
\newcommand{\title@note@fmt}{\renewcommand{\thefootnote}{\fnstar{footnote}}}
\newcommand{\author@note@fmt}{\setcounter{footnote}{0}%
           \renewcommand\thefootnote{\alph{footnote}}}
\newcommand{\note@sep}{,}                                % Footnote separator
\renewcommand{\footnoterule}{\kern-3\p@
            \hrule \@width 3pc%                          % The \hrule has default \@height of 0.4pt.
            \kern 2.6\p@}
\newcommand{\fn@presym}{}                                % Prefix to footnotes
\renewcommand{\@makefnmark}{\,\hbox{$^{\fn@presym%
           \mathrm{\@thefnmark}}$}\,}                    % Create footnote symbol
\newcommand{\@makefntext}[1]{\noindent\hbox to 0.75em%
           {$^{\fn@presym\mathrm{\@thefnmark}}$\hss}#1}  % Format of footnote list
\renewcommand\footnotemark{\@ifnextchar[{\@xfootnotemark%
    }{\refstepcounter{footnote}\xdef\@thefnmark{\thefootnote}\@footnotemark}}%

\newcommand{\fnstar}[1]{\@fnstar{\@nameuse{c@#1}}}
\newcommand{\@fnstar}[1]{%
           \ifcase#1\or
             \hbox{$\star$}\or
             \hbox{$\star\star$}\or
             \hbox{$\star\star\star$}\or
             \hbox{$\star\star\star\star$}\or
             \hbox{$\star\star\star\star\star$}\or
             \hbox{$\star\star\star\star\star\star$}
           \else
             \@ctrerr
           \fi
           \relax}
\newcommand{\astsymbol}[1]{\@astsymbol{\@nameuse{c@#1}}}
\newcommand{\@astsymbol}[1]{%
           \ifcase#1\or
             \hbox{$\ast$}\or
             \hbox{$\ast\ast$}\or
             \hbox{$\ast\ast\ast$}\or
             \hbox{$\ast\ast\ast\ast$}\or
             \hbox{$\ast\ast\ast\ast\ast$}\or
             \hbox{$\ast\ast\ast\ast\ast\ast$}%
           \else
             \@ctrerr
           \fi
           \relax}
\renewcommand{\@alph}[1]{%
           \ifcase#1\or a\or b\or c\or d\or e\or f\or g\or h\or i\or j\or
             k\or \ell\or m\or n\or o\or p\or q\or r\or s\or t\or u\or v\or w\or x\or
             y\or z\or aa\or ab\or ac\or ad\or ae\or af\or ag\or ah\or ai\or aj\or
             ak\or a\ell\or am\or an\or ao\or ap\or aq\or ar\or as\or at\or au\or av\or
             aw\or ay\or az\or ba\or bb\or bc\or bd\or be\or bf\or bg\or bh\or bi\or
             bj\or bk\or b\ell\or bm\or bn\or bo\or bp\or bq\or br\or bs\or bt\or
             bu\or bw\or bx\or by\or bz\or ca\or cb\or cc\or cd\or ce\or cf\or cg\or
             ch\or ci\or cj\or ck\or c\ell\or cm\or cn\or co\or cp\or cq\or cr\or
             cs\or ct\or cu\or cw\or cx\or cy\or cz\or da\or db\or dc\or dd\or de\or
             df\or dg\or dh\or di\or dj\or dk\or d\ell\or dm\or dn\or do\or dp\or
             dq\or dr\or ds\or dt\or du\or dw\or dx\or dy\or dz\or ea\or eb\or ec\or
             ed\or ee\or ef\or eg\or eh\or ei\or ej\or ek\or e\ell\or em\or en\or
             eo\or ep\or eq\or er\or es\or et\or eu\or ew\or ex\or ey\or ez
          \else
             \@ctrerr
          \fi}

%% FOOTNOTES FOR THE FRONTMATTER
\newtoks\t@glob@notes                               % Accumulative List of all notes
\newcommand{\output@glob@notes}{\bgroup%
                        \the\t@glob@notes%
                        \egroup}


\def\@substring #1{\expandafter\@subs #1\endsubs}
\def\@subs #1#2\endsubs {#1}

\def\@delname #1 #2{#2}
\def\@delfirstname#1{\expandafter\@delname #1}

%% RUNNING AUTHORS
\newcommand{\runauthor@fmt}{\begingroup\no@harm%
            \if@firstauthor                                                    % IF first author
               \ifnum0\n@author@ > 3                                           % AND > 2 authors
                  \global\edef\@runauthor{\@delfirstname{\@author} \ et al.}%  % Only first author
               \else
                  \global\edef\@runauthor{\@delfirstname{\@author}}%          % ELSE just add author to list
               \fi
            \else
               \ifnum0\n@author@ < 4                                           % IF less than 3 authors
                  \ifnum0\theauthor = \n@author@                               % AND Last author
                     \ifnum0\theauthor = 2
                        \global\edef\@runauthor{\@runauthor\ and \@delfirstname{\@author}}%
                     \else
                        \global\edef\@runauthor{\@runauthor,\ and \@delfirstname{\@author}}%
                     \fi
                  \else
                     \global\edef\@runauthor{\@runauthor, \@delfirstname{\@author}}%    % ELSE add a comma
                  \fi
               \fi
            \fi
            \endgroup}


%% MISC DEFINITIONS USED IN FRONTMATTER PLACES

% make a few instructions harmless to avoid problems
\newcommand\no@harm{%
        \let\\=\relax  \let\rm\relax
        \let\ss=\relax \let\ae=\relax \let\oe=\relax
        \let\AE=\relax \let\OE=\relax
        \let\o=\relax  \let\O=\relax
        \let\i=\relax  \let\j=\relax
        \let\aa=\relax \let\Av=\relax
        \let\l=\relax  \let\L=\relax
        \let\d=\relax  \let\b=\relax \let\c=\relax
        \let\bar=\relax \let\EE=\relax
        \def\protect{\noexpand\protect\noexpand}}

% Globally defines #1 (\xdef\#1\)
\newcommand{\@xnamedef}[1]{\expandafter\xdef\csname #1\endcsname}%

\renewcommand{\ps@plain}{
\if@twoside
    \renewcommand{\@oddhead}{}
    \renewcommand{\@evenhead}{}
    \renewcommand{\@oddfoot}{\hfil\@pagenumberstyle\thepage}
    \renewcommand{\@evenfoot}{\@pagenumberstyle\thepage\hfil}
\else
    \renewcommand{\@oddhead}{}
    \renewcommand{\@evenhead}{}
    \renewcommand{\@oddfoot}{\hfil\@pagenumberstyle\thepage\hfil}
    \renewcommand{\@evenfoot}{\hfil\@pagenumberstyle\thepage\hfil}
\fi}

%% FIGURE ENVIRONMENT
\newcounter{figure}
\renewcommand \thefigure {\@arabic\c@figure}
\def\fps@figure{tbp}
\def\ftype@figure{1}
\def\ext@figure{lof}
\def\fnum@figure{\figurename\nobreakspace\thefigure}
\newenvironment{figure}
               {\let\@makecaption\@makefigurecaption
                \def\@floatboxreset{\old@floatboxreset\centering}
                \@float{figure}}
               {\end@float}
\newenvironment{figure*}
               {\let\@makecaption\@makefigurecaption
                \def\@floatboxreset{\old@floatboxreset\centering}
                \@dblfloat{figure}}
               {\end@dblfloat}

%% TABLE ENVIRONMENT
\newcounter{table}
\renewcommand\thetable{\@arabic\c@table}
\def\fps@table{tbp}
\def\ftype@table{2}
\def\ext@table{lot}
\def\fnum@table{{\bfseries\tablename\nobreakspace\thetable}}
\let\old@floatboxreset\@floatboxreset
\newenvironment{table}
               {\let\@makecaption\@maketablecaption
                \def\@floatboxreset{\old@floatboxreset\centering\@tablesize}
                \@float{table}}
               {\end@float}
\newenvironment{table*}
               {\let\@makecaption\@maketablecaption
                \def\@floatboxreset{\old@floatboxreset\centering\@tablesize}
                \@dblfloat{table}}
               {\end@dblfloat}

%% CAPTION COMMAND
\long\def\@makefigurecaption#1#2{%
  \vskip\abovecaptionskip
  \sbox\@tempboxa{{\@captionstyle #1}. {\@captionsize #2}}%
  \ifdim \wd\@tempboxa >\hsize
    \ifdim \hsize=\textwidth
        \leftskip\@figureindent
        \rightskip\@figureindent
        {\@captionstyle #1}. {\@captionsize #2}\par
    \else
        {\@captionstyle #1}. {\@captionsize #2}\par
    \fi
  \else
    \global \@minipagefalse
    \ifdim \hsize=\textwidth
        \leftskip 10mm
        \rightskip 10mm
        \hb@xt@\hsize{\box\@tempboxa\hfil}%
    \else
        \hb@xt@\hsize{\box\@tempboxa\hfil}%
    \fi
  \fi
  \vskip\belowcaptionskip}

\long\def\@maketablecaption#1#2{%
  \sbox\@tempboxa{{\@captionstyle #1}. {\@captionsize #2}}%
  \ifdim \wd\@tempboxa >\hsize
    \ifdim \hsize=\textwidth
        %\leftskip\@figureindent
        %\rightskip\@figureindent
        {\@captionstyle #1}. {\@captionsize #2}\par
    \else
        {\@captionstyle #1}. {\@captionsize #2}\par
    \fi
  \else
    \global \@minipagefalse
    \ifdim \hsize=\textwidth
        \leftskip 10mm
        \rightskip 10mm
        \hb@xt@\hsize{\box\@tempboxa\hfil}%
    \else
        \hb@xt@\hsize{\box\@tempboxa\hfil}%
    \fi
  \fi
  \vskip\belowcaptionskip}

%% VERSE ENVIRONEMNT
\newenvironment{verse}
               {\let\\\@centercr
                \list{}{\itemsep      \z@
                        \itemindent   -1.5em%
                        \listparindent\itemindent
                        \rightmargin  \leftmargin
                        \advance\leftmargin 1.5em}%
                \item\relax}
               {\endlist}

%% QUOTATION ENVIRONEMNT
\newenvironment{quotation}
               {\list{}{\listparindent 1.5em%
                        \itemindent    \listparindent
                        \rightmargin   \leftmargin
                        \parsep        \z@ \@plus\p@}%
                \item\relax}
               {\endlist}

%% QUOTE ENVIRONMENT
\newenvironment{quote}
               {\list{}{\rightmargin\leftmargin}%
                \item\relax}
               {\endlist}

%% DECRIPTION ENVIRONEMNT
\newenvironment{description}
               {\list{}{\labelwidth\z@ \itemindent-\leftmargin
                        \let\makelabel\descriptionlabel}}
               {\endlist}
\newcommand*\descriptionlabel[1]{\hspace\labelsep
                                \normalfont\bfseries #1}

% LIST SETTINGS
\setlength\partopsep{2\p@ \@plus 1\p@ \@minus 1\p@}

\if@twocolumn
  \setlength\leftmargini  {2em}
\else
  \setlength\leftmargini  {2.5em}
\fi
\leftmargin  \leftmargini
\setlength\leftmarginii  {2.2em}
\setlength\leftmarginiii {1.87em}
\setlength\leftmarginiv  {1.7em}
\if@twocolumn
  \setlength\leftmarginv  {.5em}
  \setlength\leftmarginvi {.5em}
\else
  \setlength\leftmarginv  {1em}
  \setlength\leftmarginvi {1em}
\fi
\setlength  \labelsep  {.5em}
\setlength  \labelwidth{\leftmargini}
\addtolength\labelwidth{-\labelsep}
\@beginparpenalty -\@lowpenalty
\@endparpenalty   -\@lowpenalty
\@itempenalty     -\@lowpenalty
\renewcommand\theenumi{\@arabic\c@enumi}
\renewcommand\theenumii{\@alph\c@enumii}
\renewcommand\theenumiii{\@roman\c@enumiii}
\renewcommand\theenumiv{\@Alph\c@enumiv}
\newcommand\labelenumi{\theenumi.}
\newcommand\labelenumii{(\theenumii)}
\newcommand\labelenumiii{\theenumiii.}
\newcommand\labelenumiv{\theenumiv.}
\renewcommand\p@enumii{\theenumi}
\renewcommand\p@enumiii{\theenumi(\theenumii)}
\renewcommand\p@enumiv{\p@enumiii\theenumiii}
\newcommand\labelitemi{\textbullet}
\newcommand\labelitemii{\normalfont\bfseries \textendash}
\newcommand\labelitemiii{\textasteriskcentered}
\newcommand\labelitemiv{\textperiodcentered}

\setlength\partopsep{2\p@ \@plus 1\p@ \@minus 1\p@}
\def\@listi{\leftmargin\leftmargini
            \parsep 4\p@ \@plus2\p@ \@minus\p@
            \topsep 8\p@ \@plus2\p@ \@minus4\p@
            \itemsep4\p@ \@plus2\p@ \@minus\p@}

\let\@listI\@listi
\@listi
\def\@listii {\leftmargin\leftmarginii
              \labelwidth\leftmarginii
              \advance\labelwidth-\labelsep
              \topsep    4\p@ \@plus2\p@ \@minus\p@
              \parsep    2\p@ \@plus\p@  \@minus\p@
              \itemsep   \parsep}
\def\@listiii{\leftmargin\leftmarginiii
              \labelwidth\leftmarginiii
              \advance\labelwidth-\labelsep
              \topsep    2\p@ \@plus\p@\@minus\p@
              \parsep    \z@
              \partopsep \p@ \@plus\z@ \@minus\p@
              \itemsep   \topsep}
\def\@listiv {\leftmargin\leftmarginiv
              \labelwidth\leftmarginiv
              \advance\labelwidth-\labelsep}
\def\@listv  {\leftmargin\leftmarginv
              \labelwidth\leftmarginv
              \advance\labelwidth-\labelsep}
\def\@listvi {\leftmargin\leftmarginvi
              \labelwidth\leftmarginvi
              \advance\labelwidth-\labelsep}

%% APPENDIX COMMAND
\def\app@number#1{\setcounter{#1}{0}%
  \@addtoreset{#1}{section}%
  \@namedef{the#1}{\@Alph\c@section.\arabic{#1}}}

\newcommand\appendix{\cleardoublepage\par
  \setcounter{section}{0}%
  \setcounter{subsection}{0}%
  \gdef\thesection{\appendixname\space\@Alph\c@section:}
  \gdef\thesubsection   {\@Alph\c@section.\@arabic\c@subsection.}
  \gdef\thesubsubsection{\thesubsection\@arabic\c@subsubsection.}
  \gdef\theparagraph    {\thesubsubsection\@arabic\c@paragraph.}
  \gdef\thesubparagraph {\theparagraph\@arabic\c@subparagraph.}
  \app@number{equation}\app@number{figure}\app@number{table}}%


%% TABLE OF CONTENTS
\newcommand\tableofcontents{%
    \section*{\contentsname
        \@mkboth{%
           \MakeUppercase\contentsname}{\MakeUppercase\contentsname}}%
    \@starttoc{toc}%
    }

%% LIST OF FIGURES & LIST OF TABLES
\newcommand*\l@figure{\@dottedtocline{1}{1.5em}{2.3em}}
\newcommand\listoftables{%
    \section*{\listtablename}%
      \@mkboth{%
          \MakeUppercase\listtablename}%
         {\MakeUppercase\listtablename}%
    \@starttoc{lot}%
    }
\let\l@table\l@figure

%% SETTINGS FOR LIST OF FIGURES, TABLES, AND TABLE OF CONTENT
\setlength\arraycolsep{5\p@}
\setlength\tabcolsep{6\p@}
\setlength\arrayrulewidth{.4\p@}
\setlength\doublerulesep{2\p@}
\setlength\tabbingsep{\labelsep}
\skip\@mpfootins = \skip\footins
\setlength\fboxsep{3\p@}
\setlength\fboxrule{.4\p@}
\renewcommand \theequation {\@arabic\c@equation}

\newcommand\@pnumwidth{1.55em}
\newcommand\@tocrmarg{2.55em}
\newcommand\@dotsep{4.5}
\setcounter{tocdepth}{3}

\newcommand*\l@part[2]{%
  \ifnum \c@tocdepth >-2\relax
    \addpenalty\@secpenalty
    \addvspace{2.25em \@plus\p@}%
    \setlength\@tempdima{3em}%
    \begingroup
      \parindent \z@ \rightskip \@pnumwidth
      \parfillskip -\@pnumwidth
      {\leavevmode
       \large \bfseries #1\hfil \hb@xt@\@pnumwidth{\hss #2}}\par
       \nobreak
    \endgroup
  \fi}

\newcommand*\l@section[2]{%
  \ifnum \c@tocdepth >\z@
    \addpenalty\@secpenalty
    \addvspace{1.0em \@plus\p@}%
    \setlength\@tempdima{1.5em}%
    \begingroup
      \parindent \z@ \rightskip \@pnumwidth
      \parfillskip -\@pnumwidth
      \leavevmode \bfseries
      \advance\leftskip\@tempdima
      \hskip -\leftskip
      #1\nobreak\hfil \nobreak\hb@xt@\@pnumwidth{\hss #2}\par
    \endgroup
  \fi}
\newcommand*\l@subsection{\@dottedtocline{2}{1.5em}{2.3em}}
\newcommand*\l@subsubsection{\@dottedtocline{3}{3.8em}{3.2em}}
\newcommand*\l@paragraph{\@dottedtocline{4}{7.0em}{4.1em}}
\newcommand*\l@subparagraph{\@dottedtocline{5}{10em}{5em}}
\newcommand\listoffigures{%
    \section*{\listfigurename}%
      \@mkboth{\MakeUppercase\listfigurename}%
              {\MakeUppercase\listfigurename}%
    \@starttoc{lof}%
    }

%% THE BIBLOGRAPHY
\newif\if@nameyear
\@nameyeartrue
\if@nameyear
    \def\@biblabel#1{}
\else
    \def\@biblabel#1{[#1]\hskip \z@ \@plus 1filll}
\fi

\newdimen\bibindent
\setlength\bibindent{1.5em}
\newenvironment{thebibliography}[1]
     { \@startsection{section}{1}{\z@}{-1\baselineskip \@plus 0.3\baselineskip \@minus 0.1\baselineskip}
        {0.5\baselineskip}
        {\raggedright\large\bfseries\hyphenpenalty\@M}*{\refname}%
      \addcontentsline{toc}{section}{\refname}
      \@mkboth{\MakeUppercase\refname}{\MakeUppercase\refname}%
      \@bibliosize
      \list{\@biblabel{\@arabic\c@enumiv}}%
           {\settowidth\labelwidth{\@biblabel{#1}}%
              \labelsep 3\p@ \itemindent\z@
              \if@nameyear
                \labelwidth\z@ \labelsep\z@ \leftmargin\parindent
                \itemindent-\parindent
              \else
                \labelsep 3\p@ \itemindent\z@
                \leftmargin\labelwidth \advance\leftmargin\labelsep
              \fi
            \setlength{\itemsep}{0\z@}      % No glue between reference items
            % \interlinepenalty=10000         % Do not allow breaks in a reference
            \baselineskip=9pt plus .001\p@ minus 0.25\p@ % Allow some baseline stretch
            \@openbib@code
            \usecounter{enumiv}%
            \let\p@enumiv\@empty
            \renewcommand\theenumiv{\@arabic\c@enumiv}}%
            \@openbib@code
      \sloppy
      \clubpenalty1000
      \widowpenalty1000
      \@clubpenalty \clubpenalty
      \setlength{\emergencystretch}{2pc}
      \hbadness5000
      \sfcode`\.\@m}
     {\def\@noitemerr
       {\@latex@warning{Empty `thebibliography' environment}}%
      \endlist}

\let\@openbib@code\@empty
\newcommand\newblock{\hskip .11em\@plus.33em\@minus.07em}

%% THE INDEX
\newenvironment{theindex}
               {\if@twocolumn
                  \@restonecolfalse
                \else
                  \@restonecoltrue
                \fi
                \twocolumn[\section*{\indexname}]%
                \@mkboth{\MakeUppercase\indexname}%
                        {\MakeUppercase\indexname}%
                \thispagestyle{plain}\parindent\z@
                \parskip\z@ \@plus .3\p@\relax
                \columnseprule \z@
                \columnsep 35\p@
                \let\item\@idxitem}
               {\if@restonecol\onecolumn\else\clearpage\fi}

\newcommand\@idxitem{\par\hangindent 40\p@}
\newcommand\subitem{\@idxitem \hspace*{20\p@}}
\newcommand\subsubitem{\@idxitem \hspace*{30\p@}}
\newcommand\indexspace{\par \vskip 10\p@ \@plus5\p@ \@minus3\p@\relax}

%% ACKNOWLEDGEMENTs ENVIRONMENT
\newenvironment{acknowledgements}{\par
    \vspace{1.5\baselineskip \@plus .5\baselineskip \@minus .5\baselineskip}
    \parfillskip\@flushglue                         % Horisontal space on last line of paragraph
    \@acknowledgestyle                              % Text size of the ackknowledgement
    \parskip\z@                                     % The space between paragraphs
    \noindent\@acknowledgementheading               % Caption for ackknowledgement
    \ignorespaces}
{\par}

%% PAPER ENVIRONEMNT

\newcounter{c@paper}
\newenvironment{paper}
               {\list{\bfseries\Roman{c@paper}}{\usecounter{c@paper}
                        \setlength{\topsep}{\baselineskip}
                        \itemindent-\leftmargin
                        \setlength{\labelsep}{1em}
                        \addtolength{\leftmargin}{\@abstractrightskip}
                        \rightmargin\leftmargin
                        \addtolength{\leftmargin}{-\itemindent}
                        \parfillskip\@flushglue
                        \interlinepenalty=10000
                        \ignorespaces
                        }}
               {\endlist}


\newenvironment{paper*}
               {\list{}{\labelwidth\z@
                        \itemindent-\leftmargin
                        \rightmargin\leftmargin
                        \parfillskip\@flushglue
                        \baselineskip=10\p@
                        \interlinepenalty=10000
                        \ignorespaces
                        }}
               {\endlist}

\newenvironment{dissertationseries}[1]
               {\renewcommand{\thefootnote}{\fnsymbol{footnote}}
                \cleardoublepage
                \if@twocolumn             % Temporary switches of two-column mode
                    \@restonecoltrue\onecolumn
                \else
                    \@restonecolfalse
                \fi
                \pagestyle{empty}
                \vspace{1\baselineskip}
                \centering\vbox{\bfseries#1}
                \list{}{ \itemindent-\leftmargin
                        \parfillskip\@flushglue
                        \baselineskip=10\p@
                        \interlinepenalty=10000
                        \ignorespaces}}
               {\endlist
                \if@twocolumn             % Temporary switches of two-column mode
                    \@restonecoltrue\onecolumn
                \else
                    \@restonecolfalse
                \fi}


\RequirePackage{color}
\RequirePackage{type1cm}
\newdimen\@Rulewidth
\newdimen\@OddBoxLength
\newdimen\@EvenBoxLength
\setlength{\@Rulewidth}{15mm}
\setlength{\@OddBoxLength}{1in}
\addtolength{\@OddBoxLength}{5mm}
\setlength{\@EvenBoxLength}{1in}
\addtolength{\@EvenBoxLength}{5mm}
\definecolor{INKgray}{rgb}{0.7,0.7,0.7}

\newcommand{\paperpage}[1]{\cleardoublepage
                \if@twoside
                    \ifodd\c@page
                    \else
                        \newpage
                        \thispagestyle{empty}
                        \if@twocolumn
                            \newpage
                            \thispagestyle{empty}
                        \fi
                    \fi
                \fi
           \thispagestyle{empty}
           \if@twocolumn            % Temporary switches of two-column mode
                \@restonecoltrue\onecolumn
           \else
             \@restonecolfalse
           \fi
                \@tempdima=\textheight
                \divide \@tempdima by 6
                \@tempdimb=\@Rulewidth
                \multiply \@tempdimb by #1
                \advance \@tempdimb 4mm
                \advance \@tempdima by \@tempdimb
                \vspace*{\@tempdima}
                \raggedleft
                \fontsize{48}{0}\sl\textsf{Paper~#1}
                \color{INKgray}\mbox{\color@block{\@OddBoxLength}{\@Rulewidth}{4mm}}
                \normalcolor
           \newpage
           \thispagestyle{empty}
                \vspace*{\@tempdima}
                \raggedright
                \hspace{-\@EvenBoxLength}
                \color{INKgray}\mbox{\color@block{\@EvenBoxLength}{\@Rulewidth}{4mm}}
                \normalcolor\normalfont\normalsize
           \if@restonecol         % Restores two-column mode
               \twocolumn
               \newpage
           \else
             \newpage
           \fi}

%% MISC DEFINITIONS
\def\cleardoublepage{\clearpage\if@twoside \ifodd\c@page\else
\hbox{} \thispagestyle{empty}
\newpage
\if@twocolumn\hbox{}\newpage\fi\fi\fi}

\newcommand{\today}{%
            \ifcase\month\or
                January\or February\or March\or April\or May\or June\or
                July\or August\or September\or October\or November\or December
            \fi
            \space\number\day, \number\year}

\AtEndDocument{\cleardoublepage
                \addtocounter{page}{-1}%
                \immediate\write\@auxout{\string\global\string\c@lastpage=\the\c@page}%
                \addtocounter{page}{1}
                }
