#!/usr/bin/env ruby
# frozen_string_literal: true

TAGS = 'tags'

def parse_tag_line(part1, part2, typeinfo, fileinfo)
  puts part1, part2
  basic_info = part1.split('\t')
  tagname = basic_info[0]
  filename = basic_info[1]

  pattern = basic_info[2...-1].join('\t')
  if pattern[0] == '/'
    start = 2
    # end = pattern.length -1
  end
end

def filter_tags(lines)
  typeinfo = {}
  fileinfo = {}

  lines.each do |line|
    next if line =~ /^!_TAG_/

    parts = line.split(';"')
    parse_tag_line(parts[0], parts[1], typeinfo, fileinfo) if parts.length == 2
  end
end

def signals
  Signal.trap('PIPE', 'EXIT')
end

def main
  signals

  lines = File.readlines(TAGS)
  filter_tags(lines)
end

main if __FILE__ == $PROGRAM_NAME
