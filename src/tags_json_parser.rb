#!/usr/bin/env ruby
# frozen_string_literal: true

require 'json'

TAGS = 'ctags.json'

def signals
  Signal.trap('PIPE', 'EXIT')
end

# Only for cpp
# TODO(Drogon): template
# TODO(Drogon): virtual
# TODO(Drogon): 构建全局的拓扑 class name 然后通过全局的map 来做， 留一个context

class NameSpace
  def initialize
    @classes = []
    @variables = []
  end

end

class Class
  # is_struct
  def initialize
    @members = []
  end
end

class Enum
end

class TagsParser
  def initialize(tags_file)
    @tags_json = _parse_tags(tags_file)
    # pp @tags_json[0]
  end

  def process
    @tags_json.each do |tag|
      class_name = tag['name']
      baseclass_name = tag['inherits']
      filename = tag['path']
      if baseclass_name && filename !=~ /_test.cc$/ && !class_name.include?('::')
        pp tag
        # pp baseclass_name

        # pp tag
        puts "#{baseclass_name} <|-- #{class_name}"
      end
    end
  end

private

  def _parse_tags tags_file
    tags_file.readlines.map { |line| JSON.parse line }
  end
end

def main
  signals

  file = $stdin
  file = File.open TAGS if File.exist? TAGS
  tags_parser = TagsParser.new(file)

  tags_parser.process
end

main if __FILE__ == $PROGRAM_NAME

__END__
{"_type"=>"tag",
 "name"=>"AcceptAndReply",
 "path"=>"raft/raft_paper_test.cc",
 "pattern"=>
  "/^  static std::unique_ptr<Message> AcceptAndReply(std::unique_ptr<Message> msg) {$/",
 "file"=>true,
 "typeref"=>"typename:std::unique_ptr<Message>",
 "kind"=>"function",
 "scope"=>"byteraft::ConsensusTest",
 "scopeKind"=>"class"}

tagname = name
filename = path
