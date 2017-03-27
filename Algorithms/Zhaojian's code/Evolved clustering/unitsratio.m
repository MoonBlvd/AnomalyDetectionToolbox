function ratio = unitsratio(to, from)
%UNITSRATIO Unit conversion factors
%
%   RATIO = UNITSRATIO(TO, FROM) returns the number of TO units per one
%   FROM unit.  For example, UNITSRATIO('cm', 'm') returns 100 because
%   there are 100 centimeters per meter.  UNITSRATIO makes it easy to
%   convert from one system of units to another.  Specifically, if X is
%   in units FROM and
%
%                  Y = UNITSRATIO(TO, FROM) * X,
%
%   then Y is in units TO.
%
%   TO and FROM may be any strings from the second column of one of the
%   following tables. (Both must come from the same table.)  TO and FROM
%   are case-insensitive and may be either singular or plural.
%
%   Units of Length
%   ---------------
%
%     Unit Name            String(s)
%     ---------            ---------
%     meter                'm', 'meter(s)', 'metre(s)'
%
%     centimeter           'cm', 'centimeter(s)', 'centimetre(s)'
%
%     millimeter           'mm', 'millimeter(s)', 'millimetre(s)'
%
%     micron               'micron(s)'
%
%     kilometer            'km', 'kilometer(s)', 'kilometre(s)'
%
%     nautical mile        'nm', 'nautical mile(s)
%
%     international foot   'ft',   'international ft',
%                          'foot', 'international foot',
%                          'feet', 'international feet'
%
%     inch                 'in', 'inch', 'inches'
%
%     yard                 'yd', 'yard(s)'
%
%     international mile   'mi', 'mile(s)', 'international mile(s)'
%
%     U.S. survey foot     'sf',
%                          'survey ft',   'U.S. survey ft',
%                          'survey foot', 'U.S. survey foot',
%                          'survey feet', 'U.S. survey feet',
%
%     U.S. survey mile     'sm', 'survey mile(s)', 'statute mile(s)',
%     (statute mile)       'U.S. survey mile(s)'
%
%
%   Units of Angle
%   ---------------
%
%     Unit Name            String(s)
%     ---------            ---------
%     radian               'rad', 'radian(s)'
%     degree               'deg', 'degree(s)'
%
%
%   Examples
%   --------
%   % Approximate mean earth radius in meters
%   radiusInMeters = 6371000
%   % Conversion factor
%   feetPerMeter = unitsratio('feet', 'meter')
%   % Radius in (international) feet:
%   radiusInFeet = feetPerMeter * radiusInMeters
%
%   % The following prints a true statement for any valid TO, FROM pair:
%   to   = 'feet';
%   from = 'mile';
%   sprintf('There are %g %s per %s.', unitsratio(to,from), to, from)
%
%   % The following prints a true statement for any valid TO, FROM pair:
%   to   = 'degrees';
%   from = 'radian';
%   sprintf('One %s is %g %s.', from, unitsratio(to,from), to)

% Copyright 1996-2006 The MathWorks, Inc.
% $Revision: 1.1.8.3 $ $Date: 2006/05/24 03:36:54 $

% Exact definitions: Each unit on the left is defined in terms of the unit
% on the right via the factor provided, which is the value that will be
% computed by 1 / UNITSRATIO(LEFT,RIGHT).   [Note the inverse.]
% (All strings must be in lower case only.)

global definitions synonyms
if isempty(definitions) || isempty(synonyms)

   definitions.micron.m = 1e-6;
   definitions.mm.m = 1e-3;
   definitions.cm.m = 1e-2;
   definitions.km.m = 1e3;
   definitions.nm.m = 1852;
   definitions.ft.m = 0.3048;
   definitions.sf.m = 1200/3937;
   definitions.mi.ft = 5280;
   definitions.sm.sf = 5280;
   definitions.in.ft = 1/12;
   definitions.yd.ft = 3;
   definitions.deg.rad = pi/180;

   % include reverse conversions in definitions
   fromFields = fieldnames(definitions);
   for fromIdx = 1:length(fromFields)
      toFields = fieldnames(definitions.(fromFields{fromIdx}));
      for toIdx = 1:length(toFields)
         definitions.(toFields{toIdx}).(fromFields{fromIdx}) = 1/definitions.(fromFields{fromIdx}).(toFields{toIdx});
      end
   end

   % synonyms
   synonyms.meter              = 'm';
   synonyms.metre              = 'm';
   synonyms.centimeter         = 'cm';
   synonyms.centimetre         = 'cm';
   synonyms.millimeter         = 'mm';
   synonyms.millimetre         = 'mm';
   synonyms.kilometer          = 'km';
   synonyms.kilometre          = 'km';
   synonyms.nauticalmile       = 'nm';
   synonyms.inch               = 'in';
   synonyms.inches             = 'in';
   synonyms.yard               = 'yd';
   synonyms.internationalft    = 'ft';
   synonyms.foot               = 'ft';
   synonyms.internationalfoot  = 'ft';
   synonyms.feet               = 'ft';
   synonyms.internationalfeet  = 'ft';
   synonyms.mile               = 'mi';
   synonyms.internationalmile  = 'mi';
   synonyms.surveyft           = 'sf';
   synonyms.ussurveyft         = 'sf';
   synonyms.surveyfoot         = 'sf';
   synonyms.ussurveyfoot       = 'sf';
   synonyms.surveyfeet         = 'sf';
   synonyms.ussurveyfeet       = 'sf';
   synonyms.surveymile         = 'sm';
   synonyms.statutemile        = 'sm';
   synonyms.ussurveymile       = 'sm';
   synonyms.radian             = 'rad';
   synonyms.degree             = 'deg';

end

% check class of TO and FROM
if ~ischar(to)
   error('Input argument ''to'' must be a string.');
end

if ~ischar(from)
   error('Input argument ''from'' must be a string.');
end

% attempt to convert synomyms to 'standard abbreviations', if necessary.
fromStandard = findSynonym(from);
toStandard   = findSynonym(to);

% recursively search for a path from "from" to "to"
ratio = searchgraph(fromStandard, toStandard, definitions, {});

% An empty return value indicates that no connection exists.
if isempty(ratio)
   error('Unable to convert from %s to %s.', from, to);
end

%-------------------------------------------------------------------

   function unitOut = findSynonym(unitIn)

      unitOut = regexprep(lower(unitIn), '[^a-z]', '');
      if ~isfield(definitions, unitOut)
         if isfield(synonyms, unitOut)
            unitOut = synonyms.(unitOut);
         elseif unitOut(end) == 's'
            unitOut = findSynonym(unitOut(1:end-1));
         else
            error('Unit %s is not supported.', unitIn);
         end
      end

   end

end

%-------------------------------------------------------------------

function [ratio, history] = searchgraph(fromIn, toIn, definitions, history)

if strcmp(fromIn, toIn)
   ratio = 1;
   return
end

ratio = [];

% Stop here if fromIn has already been checked (avoid loops in the graph).
if ismember(fromIn, history)
   return
end

% Append fromIn toIn the list of nodes that have been visited.
history{end+1} = fromIn;

% Find occurrences of fromIn and toIn in columns 1 and 2 of GRAPH.
if isfield(definitions, fromIn) && isfield(definitions.(fromIn), toIn)
   ratio = definitions.(fromIn).(toIn);
   return
end

% recursive search for conversion
toFields = fieldnames(definitions.(fromIn));
for idx = 1:length(toFields)
   [ratio, history] = searchgraph(toFields{idx}, toIn, definitions, history);
   if ~isempty(ratio)
      ratio = ratio * definitions.(fromIn).(toFields{idx});
      definitions.(fromIn).(toIn) = ratio; % add conversion to definisions (trade off memory for speed)
      return
   end
end

end

