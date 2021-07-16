#!/usr/bin/env ruby
# -*- coding:utf-8 -*-

m = {}
file = STDIN
if ARGV.length > 0
  file = File.open(ARGV[0])
end

file.each_line do |line|
  class_name, file = line.split(",")
  module_name = file.split("/")[0]
  m[module_name] ||= []
  m[module_name] << class_name
  # puts class_name, module_name
end

puts <<-HEADER
@startuml

set namespaceSeparator ::

namespace byteraft {
HEADER

m.each do |module_name, classes|
  puts "\n\n\n/' #{module_name} '/"
  puts "namespace #{module_name} {\n\n"

  classes.each do |class_name|
    puts <<-EOF
class #{class_name} {
}
EOF
  end

  puts "\n} /' namespace #{module_name} '/"
end

puts <<-FOOTER

} /' namespace byteraft '/
@enduml
FOOTER
