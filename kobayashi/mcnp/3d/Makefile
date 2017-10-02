##### MCNP6/Testing/KOBAYASHI/Makefile
#
# ------------------------------------------------------------------------
# Makefile for MCNP tests using Kobayashi Benchmarks
# ------------------------------------------------------------------------
#    Reference:  
#       K. Kobayashi, N. Sugimuri, Y. Nagaya,
#       "3-D Radiation Transport Benchmark Problems and Results 
#        for Simple Geometries with Void Regions",
#       OECD/NEA Report, November 2000
# ------------------------------------------------------------------------
SHELL     := /bin/sh 
OS        := $(shell uname | sed -e 's/CYGWIN.*/Windows_NT/')
MCNP_ROOT := $(shell cd /software/mcnp/MCNP_CODE/MCNP611; pwd | sed -e 's/ /\\ /g')

CASES :=  \
	prob1_abs	prob1_sct	\
	prob2_abs	prob2_sct	\
	prob3_abs	prob3_sct

NPS = 1000000

DATAPATH ?= /usr/projects/data/nuclear/mc/type1
 
      INPUT_FILES := $(patsubst %,%.txt,$(CASES) xs1 xs2)
 OUTPUT_TEMPLATES := no_outp      ### $(patsubst %,%out,$(CASES))
  MCTAL_TEMPLATES := no_mctal     ### $(patsubst %,%mctl,$(CASES))

all:    $(CASES)   results
 
cbts: $(CASES) 
	rm -rf difmKobayashi; touch difmKobayashi;  
	$(MAKE) diffs
	@ ./get_results.pl
	@ diff  Inputs/cbts_results.txt results.txt > difmKobayashi; ls -l difmKobayashi
# ------------------------------------------------------------------------
include $(MCNP_ROOT)/Testing/config/test_options.mk
 
TEST_TYPES = 
XSTYPE = 1
XSDIR  = 
# ------------------------------------------------------------------------
TEST_DEPS =
 
#
# simple runs - no dependencies on other jobs
#
$(CASES) :  %:   %.txt  xs1.txt xs2.txt
	@$(BEFORE)
	@ if [ "$(NPS)" ] ; then \
		echo "   ***** changing NPS to $(NPS) *****"; echo ""; \
		mv $@.txt  xxx.txt; \
		sed -e 's/^ *nps .*/nps $(NPS)/' xxx.txt >$@.txt; \
		rm -f xxx.txt; \
	  fi
	@$(RM)  $@.[mrso]
	$(PRUN) $(MCNP) name=$@. i=$@.txt  $(TASKS) $(EOL)
#	@$(AFTER)


results:
	@ ./get_results.pl
	@ cat  results.txt

# ------------------------------------------------------------------------
clean:	cleaner
cleaner:
	@$(RM)  *.txt  *.[mrso]
notes:
	@ echo " "
	@ echo "+----------------------------------------------------------------+"
	@ echo "| IMPORTANT NOTES:                                               |"
	@ echo "|   ... TBD ...                                                  |"
	@ echo "+----------------------------------------------------------------+"
	@ echo " "

# ------------------------------------------------------------------------
.PHONY:		all  notes  $(CASES)  results
# ========================================================================
