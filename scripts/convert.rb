def T_to_U(fileA, nuovo)
 c=open(nuovo, "w")
 doIt = false
 file=open(fileA).readlines.each do |i|

	if doIt
		i.size.times{|j|
			i[j]=i[j].upcase
			if i[j]=="T" or i[j]=="t" 
				i[j]="U"
			end
		}
		doIt=false
	end
	if i[0]=='>'
		doIt = true
	end
end
 c.write(file.join)
end	


T_to_U(ARGV[0],ARGV[1])
