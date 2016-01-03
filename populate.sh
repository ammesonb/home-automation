#!/bin/bash
function simple_store {
    table=$1
    cols=$2
    vals=$3
    psql automation -c "INSERT INTO $table ($cols) VALUES ($vals)"
}

echo "Select something to add:"
select target in $(echo "action keyword chain event greeting response clarification repetition" | tr " " "\n");
  do
    case $target in 
    action*)
        echo "Please enter an action name: "
        read a
        a=`echo $a | perl -ne "chomp and print"`
        echo "Please enter an action trigger word: "
        read t
        t=`echo $t | perl -ne "chomp and print"`
        echo "Please enter the associated function name: "
        read f
        f=`echo $f | perl -ne "chomp and print"`
        simple_store actions "action, function, trigger_word" "'$a', '$f', '$t'"
        ;;
    keyword*)
        echo "Please enter an action name to associate this keyword with: "
        read a
        a=`echo $a | perl -ne "chomp and print"`
        i=`psql automation -tc "SELECT id FROM actions WHERE action='$a'"`
        i=`echo $i | perl -ne "chomp and print"`
        if [ -z "$i" ];
          then
            echo "Invalid action";
            continue;
        fi
        echo "Please enter the keyword:"
        read k
        k=`echo $k | perl -ne "chomp and print"`
        simple_store keywords "action, keyword" "$i, '$k'"
        ;;
    chain*)
        echo "Please enter a name for the chain: "
        read n
        n=`echo $n | perl -ne "chomp and print"`
        simple_store chains "chain" "'$n'"
        ci=`psql automation -tc "SELECT id FROM chains WHERE chain='$n'"`
        ci=`echo $ci | perl -ne "chomp and print"`
        s=0
        echo "Leave action blank to finish"
        echo ""
        while true
          do
            echo "Enter action to trigger: "
            read a
            a=`echo $a | perl -ne "chomp and print"`
            if [ -z "$a" ]; then break; fi
            echo "What keyword on this action do you want to use?"
            read k
            k=`echo $k | perl -ne "chomp and print"`
            i=`psql automation -tc "SELECT id FROM actions WHERE action='$a'"`
            i=`echo $i | perl -ne "chomp and print"`
            if [ -z "$i" ];
              then
                echo "Invalid action";
                continue;
            fi
            i=`psql automation -tc "SELECT id FROM keywords WHERE action=$i and keyword='$k'"`
            i=`echo $i | perl -ne "chomp and print"`
            if [ -z "$i" ];
              then
                echo "Invalid keyword";
                continue;
            fi
            simple_store chain_actions "chain, action, seq" "$ci, $i, $s"
            ((s++))
        done
        ;;
    event*)
        echo "Please enter a chain: "
        read c
        c=`echo $c | perl -ne "chomp and print"`
        i=`psql automation -tc "SELECT id FROM chains WHERE chain='$c'"`
        i=`echo $i | perl -ne "chomp and print"`
        if [ -z "$i" ];
          then
            echo "Invalid chain";
            continue;
        fi
        echo "Please enter an event name: "
        read n
        n=`echo $n | perl -ne "chomp and print"`
        echo "Please enter a function to check trigger conditions: "
        read f
        f=`echo $f | perl -ne "chomp and print"`
        simple_store events "name, chain, function" "'$n', $i, '$f'"
        ;;
    greeting*)
        echo "Please enter a greeting: "
        read p
        p=`echo $p | perl -ne "chomp and print"`
        p=`echo $p | sed "s/'/''/g"`
        echo "What is the formality level?"
        read f
        f=`echo $f | perl -ne "chomp and print"`
        echo "What time range is acceptable?"
        read t
        t=`echo $t | sed "s/,/','2000-01-01 /"`
        t=`echo $t | sed "s/^/'2000-01-01 /"`
        t=`echo $t | sed "s/$/'/"`
        t=`echo $t | perl -ne "chomp and print"`
        simple_store greetings "phrase, formality, time_of_day" "'$g', $f, tsrange($t)"
        ;;
    response*)
        echo "Please enter a response: "
        read p
        p=`echo $p | perl -ne "chomp and print"`
        p=`echo $p | sed "s/'/''/g"`
        echo "What is the formality level?"
        read f
        f=`echo $f | perl -ne "chomp and print"`
        echo "Is this affirmative? (y/n/u)"
        read a
        a=`echo $a | perl -ne "chomp and print"`
        simple_store responses "phrase, is_affirmative, formality" "'$p', '$a', $f"
        ;;
    clarification*)
        echo "Please enter a clarification: "
        read p
        p=`echo $p | perl -ne "chomp and print"`
        p=`echo $p | sed "s/'/''/g"`
        while [[ ! $p =~ .*%s.* ]];
          do
            echo "Need %s placeholder";
            read p
            p=`echo $p | perl -ne "chomp and print"`
            p=`echo $p | sed "s/'/''/g"`
        done
        echo "What is the formality level?"
        read f
        f=`echo $f | perl -ne "chomp and print"`
        simple_store clarifications "phrase, formality" "'$p', $f"
        ;;
    repetition*)
        echo "Please enter a repeat request: "
        read p
        p=`echo $p | perl -ne "chomp and print"`
        p=`echo $p | sed "s/'/''/g"`
        echo "What is the formality level?"
        read f
        f=`echo $f | perl -ne "chomp and print"`
        simple_store repeat "phrase, formality" "'$p', $f"
        ;;
    default*)
        echo "Unrecognized mode"
        ;;
    esac
done
