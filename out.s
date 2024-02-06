
global _start
    section .bss
        termios:        resb 36
        stdin_fd:       equ 0           ; STDIN_FILENO
        ICANON:         equ 1<<1
        ECHO:           equ 1<<3
	    memo: resb 30000
    ; section .data

	; memo: times 30000 db 0

    section .text

    %include 'functions.s'
    _start:
        mov rbx, memo

        mov rdi, [rbx]
        or dil, dil
        je branch_6
    branch_0:
        call write
        call decrement
        call decrement
        call write
        call write

        mov rdi, [rbx]
        or dil, dil
        jne branch_0
    branch_6:
        call mov_right
        call mov_right
        call mov_right
        call decrement
        call mov_right
        call increment
        call mov_right
        call increment
        call increment
        call increment
        call increment
        call increment
        call mov_right
        call increment
        call increment
        call increment
        call increment
        call increment
        call increment
        call increment
        call increment
        call increment
        call increment
        call increment
        call increment
        call increment
        call increment
        call increment
        call increment
        call increment
        call increment
        call increment
        call increment
        call increment
        call increment
        call increment
        call increment
        call increment
        call increment

        mov rdi, [rbx]
        or dil, dil
        je branch_85
    branch_46:

        mov rdi, [rbx]
        or dil, dil
        je branch_56
    branch_47:
        call mov_right
        call mov_right
        call mov_right
        call increment
        call mov_left
        call mov_left
        call mov_left
        call decrement

        mov rdi, [rbx]
        or dil, dil
        jne branch_47
    branch_56:
        call mov_right
        call increment
        call increment
        call increment
        call increment
        call increment
        call mov_right
        call increment
        call mov_right
        call mov_right
        call increment

        mov rdi, [rbx]
        or dil, dil
        je branch_82
    branch_68:
        call mov_left
        call mov_left
        call increment
        call mov_right
        call mov_right
        call mov_right
        call mov_right
        call mov_right
        call increment
        call mov_left
        call mov_left
        call mov_left
        call decrement

        mov rdi, [rbx]
        or dil, dil
        jne branch_68
    branch_82:
        call mov_left
        call decrement

        mov rdi, [rbx]
        or dil, dil
        jne branch_46
    branch_85:
        call mov_right
        call mov_right
        call mov_right
        call mov_right

        mov rdi, [rbx]
        or dil, dil
        je branch_157
    branch_90:

        mov rdi, [rbx]
        or dil, dil
        je branch_103
    branch_91:
        call mov_right
        call mov_right
        call mov_right
        call increment
        call mov_right
        call increment
        call mov_left
        call mov_left
        call mov_left
        call mov_left
        call decrement

        mov rdi, [rbx]
        or dil, dil
        jne branch_91
    branch_103:
        call increment
        call increment
        call increment
        call mov_right
        call mov_right
        call increment

        mov rdi, [rbx]
        or dil, dil
        je branch_123
    branch_110:
        call mov_left
        call increment
        call mov_right
        call mov_right
        call mov_right
        call increment
        call mov_right
        call increment
        call mov_left
        call mov_left
        call mov_left
        call decrement

        mov rdi, [rbx]
        or dil, dil
        jne branch_110
    branch_123:
        call mov_right
        call mov_right

        mov rdi, [rbx]
        or dil, dil
        je branch_154
    branch_126:
        call mov_right

        mov rdi, [rbx]
        or dil, dil
        je branch_140
    branch_128:

        mov rdi, [rbx]
        or dil, dil
        je branch_138
    branch_129:
        call mov_right
        call mov_right
        call mov_right
        call increment
        call mov_left
        call mov_left
        call mov_left
        call decrement

        mov rdi, [rbx]
        or dil, dil
        jne branch_129
    branch_138:
        call mov_left

        mov rdi, [rbx]
        or dil, dil
        jne branch_128
    branch_140:
        call mov_left
        call mov_left
        call increment
        call increment
        call mov_right
        call increment
        call mov_right
        call mov_right
        call mov_right
        call mov_right
        call mov_right
        call mov_right
        call decrement

        mov rdi, [rbx]
        or dil, dil
        jne branch_126
    branch_154:
        call mov_left
        call decrement

        mov rdi, [rbx]
        or dil, dil
        jne branch_90
    branch_157:
        call increment
        call increment
        call increment
        call mov_right
        call increment
        call mov_right

        mov rdi, [rbx]
        or dil, dil
        je branch_195
    branch_164:

        mov rdi, [rbx]
        or dil, dil
        je branch_167
    branch_165:
        call decrement

        mov rdi, [rbx]
        or dil, dil
        jne branch_165
    branch_167:
        call mov_left
        call increment
        call mov_left

        mov rdi, [rbx]
        or dil, dil
        je branch_192
    branch_171:
        call mov_right
        call increment
        call increment
        call increment
        call increment
        call increment
        call increment
        call increment
        call increment
        call increment
        call increment
        call increment
        call increment
        call increment
        call increment
        call increment
        call increment
        call increment
        call mov_left
        call decrement

        mov rdi, [rbx]
        or dil, dil
        jne branch_171
    branch_192:
        call mov_left
        call increment

        mov rdi, [rbx]
        or dil, dil
        jne branch_164
    branch_195:
        call mov_right
        call mov_right

        mov rdi, [rbx]
        or dil, dil
        je branch_738
    branch_198:

        mov rdi, [rbx]
        or dil, dil
        je branch_221
    branch_199:
        call increment
        call increment
        call increment
        call increment
        call increment
        call increment
        call increment
        call increment
        call increment
        call write
        call decrement
        call decrement
        call decrement
        call decrement
        call decrement
        call decrement
        call decrement
        call decrement
        call mov_right
        call mov_right
        call mov_right

        mov rdi, [rbx]
        or dil, dil
        jne branch_199
    branch_221:
        call increment

        mov rdi, [rbx]
        or dil, dil
        je branch_228
    branch_223:
        call decrement
        call mov_left
        call mov_left
        call mov_left

        mov rdi, [rbx]
        or dil, dil
        jne branch_223
    branch_228:
        call mov_right
        call mov_right
        call mov_right

        mov rdi, [rbx]
        or dil, dil
        je branch_250
    branch_232:
        call mov_right
        call mov_right
        call read
        call decrement
        call decrement
        call decrement
        call decrement
        call decrement
        call decrement
        call decrement
        call decrement
        call decrement
        call decrement

        mov rdi, [rbx]
        or dil, dil
        je branch_248
    branch_246:
        call mov_right

        mov rdi, [rbx]
        or dil, dil
        jne branch_246
    branch_248:
        call mov_left

        mov rdi, [rbx]
        or dil, dil
        jne branch_232
    branch_250:
        call mov_left
        call mov_left

        mov rdi, [rbx]
        or dil, dil
        je branch_364
    branch_253:
        call mov_left
        call mov_left
        call mov_left

        mov rdi, [rbx]
        or dil, dil
        je branch_362
    branch_257:
        call mov_right
        call decrement
        call decrement

        mov rdi, [rbx]
        or dil, dil
        je branch_272
    branch_261:
        call mov_left
        call decrement
        call mov_right
        call mov_right
        call increment
        call mov_right
        call decrement
        call mov_left
        call mov_left
        call decrement

        mov rdi, [rbx]
        or dil, dil
        jne branch_261
    branch_272:
        call mov_left

        mov rdi, [rbx]
        or dil, dil
        je branch_299
    branch_274:

        mov rdi, [rbx]
        or dil, dil
        je branch_279
    branch_275:
        call mov_right
        call mov_right
        call mov_right

        mov rdi, [rbx]
        or dil, dil
        jne branch_275
    branch_279:
        call increment
        call mov_right
        call decrement

        mov rdi, [rbx]
        or dil, dil
        je branch_290
    branch_283:
        call increment
        call mov_right
        call mov_right
        call increment
        call mov_right
        call decrement

        mov rdi, [rbx]
        or dil, dil
        jne branch_283
    branch_290:
        call increment

        mov rdi, [rbx]
        or dil, dil
        je branch_296
    branch_292:
        call mov_left
        call mov_left
        call mov_left

        mov rdi, [rbx]
        or dil, dil
        jne branch_292
    branch_296:
        call mov_left
        call decrement

        mov rdi, [rbx]
        or dil, dil
        jne branch_274
    branch_299:
        call mov_right
        call increment
        call increment
        call mov_right

        mov rdi, [rbx]
        or dil, dil
        je branch_309
    branch_304:
        call mov_left
        call increment
        call mov_right
        call decrement

        mov rdi, [rbx]
        or dil, dil
        jne branch_304
    branch_309:
        call mov_right

        mov rdi, [rbx]
        or dil, dil
        je branch_327
    branch_311:

        mov rdi, [rbx]
        or dil, dil
        je branch_316
    branch_312:
        call mov_right
        call mov_right
        call mov_right

        mov rdi, [rbx]
        or dil, dil
        jne branch_312
    branch_316:
        call increment

        mov rdi, [rbx]
        or dil, dil
        je branch_322
    branch_318:
        call mov_left
        call mov_left
        call mov_left

        mov rdi, [rbx]
        or dil, dil
        jne branch_318
    branch_322:
        call mov_right
        call mov_right
        call mov_right
        call decrement

        mov rdi, [rbx]
        or dil, dil
        jne branch_311
    branch_327:
        call increment

        mov rdi, [rbx]
        or dil, dil
        je branch_334
    branch_329:
        call decrement
        call mov_right
        call mov_right
        call mov_right

        mov rdi, [rbx]
        or dil, dil
        jne branch_329
    branch_334:
        call mov_left
        call decrement

        mov rdi, [rbx]
        or dil, dil
        je branch_341
    branch_337:
        call increment
        call increment
        call mov_right

        mov rdi, [rbx]
        or dil, dil
        jne branch_337
    branch_341:
        call mov_right

        mov rdi, [rbx]
        or dil, dil
        je branch_351
    branch_343:
        call decrement
        call decrement
        call decrement
        call decrement
        call decrement
        call decrement
        call mov_left

        mov rdi, [rbx]
        or dil, dil
        jne branch_343
    branch_351:
        call mov_right
        call increment
        call increment
        call increment

        mov rdi, [rbx]
        or dil, dil
        je branch_360
    branch_356:
        call mov_left
        call mov_left
        call mov_left

        mov rdi, [rbx]
        or dil, dil
        jne branch_356
    branch_360:
        call mov_right

        mov rdi, [rbx]
        or dil, dil
        jne branch_257
    branch_362:
        call mov_left

        mov rdi, [rbx]
        or dil, dil
        jne branch_253
    branch_364:
        call mov_right

        mov rdi, [rbx]
        or dil, dil
        je branch_735
    branch_366:
        call decrement

        mov rdi, [rbx]
        or dil, dil
        je branch_375
    branch_368:
        call increment
        call mov_right
        call mov_right
        call increment
        call mov_right
        call decrement

        mov rdi, [rbx]
        or dil, dil
        jne branch_368
    branch_375:
        call increment
        call mov_right
        call mov_right
        call increment
        call mov_right
        call mov_right
        call mov_right
        call increment
        call mov_right

        mov rdi, [rbx]
        or dil, dil
        je branch_389
    branch_385:
        call mov_left
        call mov_left
        call mov_left

        mov rdi, [rbx]
        or dil, dil
        jne branch_385
    branch_389:
        call mov_right
        call decrement
        call mov_right
        call increment
        call mov_right

        mov rdi, [rbx]
        or dil, dil
        je branch_510
    branch_395:
        call mov_right

        mov rdi, [rbx]
        or dil, dil
        je branch_435
    branch_397:
        call decrement
        call mov_right
        call increment
        call mov_right
        call increment
        call increment
        call increment
        call mov_right
        call mov_right
        call increment
        call increment

        mov rdi, [rbx]
        or dil, dil
        je branch_413
    branch_409:
        call mov_right
        call mov_right
        call mov_right

        mov rdi, [rbx]
        or dil, dil
        jne branch_409
    branch_413:
        call increment
        call increment
        call increment
        call mov_left
        call mov_left
        call mov_left
        call increment
        call increment
        call mov_left
        call mov_left
        call mov_left
        call increment
        call increment

        mov rdi, [rbx]
        or dil, dil
        je branch_431
    branch_427:
        call mov_right
        call mov_right
        call mov_right

        mov rdi, [rbx]
        or dil, dil
        jne branch_427
    branch_431:
        call mov_right
        call mov_right
        call mov_right

        mov rdi, [rbx]
        or dil, dil
        jne branch_397
    branch_435:
        call mov_left
        call mov_left
        call mov_left

        mov rdi, [rbx]
        or dil, dil
        je branch_450
    branch_439:
        call mov_right

        mov rdi, [rbx]
        or dil, dil
        je branch_445
    branch_441:
        call mov_right
        call mov_right
        call mov_right

        mov rdi, [rbx]
        or dil, dil
        jne branch_441
    branch_445:
        call increment
        call mov_right
        call mov_right
        call mov_right

        mov rdi, [rbx]
        or dil, dil
        jne branch_439
    branch_450:
        call mov_left
        call mov_left
        call mov_left
        call mov_left
        call mov_left
        call mov_left
        call mov_left

        mov rdi, [rbx]
        or dil, dil
        je branch_490
    branch_458:
        call mov_left
        call mov_left
        call increment
        call increment
        call mov_left
        call increment

        mov rdi, [rbx]
        or dil, dil
        je branch_471
    branch_465:
        call decrement
        call mov_left
        call mov_left
        call mov_left
        call increment

        mov rdi, [rbx]
        or dil, dil
        jne branch_465
    branch_471:
        call decrement
        call mov_right
        call increment
        call increment
        call mov_right
        call mov_right
        call mov_right
        call increment
        call increment
        call mov_right
        call mov_right
        call mov_right
        call increment
        call increment
        call mov_left
        call mov_left
        call mov_left
        call mov_left

        mov rdi, [rbx]
        or dil, dil
        jne branch_458
    branch_490:
        call mov_left
        call mov_left
        call mov_left
        call increment

        mov rdi, [rbx]
        or dil, dil
        je branch_501
    branch_495:
        call decrement
        call mov_left
        call mov_left
        call mov_left
        call increment

        mov rdi, [rbx]
        or dil, dil
        jne branch_495
    branch_501:
        call increment
        call mov_right
        call decrement
        call mov_right
        call mov_right
        call decrement
        call mov_right
        call mov_right

        mov rdi, [rbx]
        or dil, dil
        jne branch_395
    branch_510:
        call mov_left
        call mov_left
        call increment
        call mov_left
        call mov_left
        call increment
        call mov_left
        call mov_left
        call mov_left
        call increment
        call mov_left
        call mov_left
        call decrement

        mov rdi, [rbx]
        or dil, dil
        je branch_531
    branch_524:
        call increment
        call mov_left
        call increment
        call mov_left
        call mov_left
        call decrement

        mov rdi, [rbx]
        or dil, dil
        jne branch_524
    branch_531:
        call increment
        call mov_left
        call increment

        mov rdi, [rbx]
        or dil, dil
        je branch_617
    branch_535:
        call decrement
        call mov_right
        call increment
        call mov_right

        mov rdi, [rbx]
        or dil, dil
        je branch_572
    branch_540:
        call decrement
        call mov_left
        call decrement
        call mov_left
        call mov_left

        mov rdi, [rbx]
        or dil, dil
        je branch_550
    branch_546:
        call mov_left
        call mov_left
        call mov_left

        mov rdi, [rbx]
        or dil, dil
        jne branch_546
    branch_550:
        call mov_right

        mov rdi, [rbx]
        or dil, dil
        je branch_571
    branch_552:
        call mov_right
        call mov_right

        mov rdi, [rbx]
        or dil, dil
        je branch_559
    branch_555:
        call mov_right
        call mov_right
        call mov_right

        mov rdi, [rbx]
        or dil, dil
        jne branch_555
    branch_559:
        call mov_left
        call mov_left
        call increment
        call mov_left

        mov rdi, [rbx]
        or dil, dil
        je branch_568
    branch_564:
        call mov_left
        call mov_left
        call mov_left

        mov rdi, [rbx]
        or dil, dil
        jne branch_564
    branch_568:
        call mov_right
        call decrement

        mov rdi, [rbx]
        or dil, dil
        jne branch_552
    branch_571:

        mov rdi, [rbx]
        or dil, dil
        jne branch_540
    branch_572:
        call mov_left

        mov rdi, [rbx]
        or dil, dil
        je branch_602
    branch_574:
        call mov_left

        mov rdi, [rbx]
        or dil, dil
        je branch_595
    branch_576:
        call mov_left

        mov rdi, [rbx]
        or dil, dil
        je branch_582
    branch_578:
        call mov_left
        call mov_left
        call mov_left

        mov rdi, [rbx]
        or dil, dil
        jne branch_578
    branch_582:
        call mov_right
        call increment
        call mov_right
        call mov_right

        mov rdi, [rbx]
        or dil, dil
        je branch_591
    branch_587:
        call mov_right
        call mov_right
        call mov_right

        mov rdi, [rbx]
        or dil, dil
        jne branch_587
    branch_591:
        call mov_left
        call mov_left
        call decrement

        mov rdi, [rbx]
        or dil, dil
        jne branch_576
    branch_595:
        call mov_left

        mov rdi, [rbx]
        or dil, dil
        je branch_601
    branch_597:
        call mov_left
        call mov_left
        call mov_left

        mov rdi, [rbx]
        or dil, dil
        jne branch_597
    branch_601:

        mov rdi, [rbx]
        or dil, dil
        jne branch_574
    branch_602:
        call mov_right
        call mov_right
        call mov_right
        call decrement
        call mov_right
        call mov_right
        call mov_right

        mov rdi, [rbx]
        or dil, dil
        je branch_614
    branch_610:
        call mov_right
        call mov_right
        call mov_right

        mov rdi, [rbx]
        or dil, dil
        jne branch_610
    branch_614:
        call increment
        call mov_right

        mov rdi, [rbx]
        or dil, dil
        jne branch_535
    branch_617:
        call mov_right
        call increment

        mov rdi, [rbx]
        or dil, dil
        je branch_628
    branch_620:
        call decrement
        call mov_left
        call mov_left

        mov rdi, [rbx]
        or dil, dil
        je branch_626
    branch_624:
        call decrement

        mov rdi, [rbx]
        or dil, dil
        jne branch_624
    branch_626:
        call mov_left

        mov rdi, [rbx]
        or dil, dil
        jne branch_620
    branch_628:
        call decrement

        mov rdi, [rbx]
        or dil, dil
        je branch_686
    branch_630:

        mov rdi, [rbx]
        or dil, dil
        je branch_635
    branch_631:
        call mov_right
        call mov_right
        call mov_right

        mov rdi, [rbx]
        or dil, dil
        jne branch_631
    branch_635:
        call mov_left

        mov rdi, [rbx]
        or dil, dil
        je branch_659
    branch_637:
        call mov_left
        call mov_left

        mov rdi, [rbx]
        or dil, dil
        je branch_644
    branch_640:
        call mov_left
        call mov_left
        call mov_left

        mov rdi, [rbx]
        or dil, dil
        jne branch_640
    branch_644:
        call mov_right
        call mov_right
        call mov_right
        call mov_right
        call mov_right
        call increment
        call mov_right

        mov rdi, [rbx]
        or dil, dil
        je branch_656
    branch_652:
        call mov_right
        call mov_right
        call mov_right

        mov rdi, [rbx]
        or dil, dil
        jne branch_652
    branch_656:
        call mov_left
        call decrement

        mov rdi, [rbx]
        or dil, dil
        jne branch_637
    branch_659:
        call mov_right
        call mov_right
        call mov_right

        mov rdi, [rbx]
        or dil, dil
        je branch_684
    branch_663:
        call mov_right

        mov rdi, [rbx]
        or dil, dil
        je branch_669
    branch_665:
        call mov_right
        call mov_right
        call mov_right

        mov rdi, [rbx]
        or dil, dil
        jne branch_665
    branch_669:
        call mov_left
        call mov_left
        call mov_left
        call mov_left
        call increment
        call mov_right

        mov rdi, [rbx]
        or dil, dil
        je branch_680
    branch_676:
        call mov_left
        call mov_left
        call mov_left

        mov rdi, [rbx]
        or dil, dil
        jne branch_676
    branch_680:
        call mov_right
        call mov_right
        call decrement

        mov rdi, [rbx]
        or dil, dil
        jne branch_663
    branch_684:
        call mov_right

        mov rdi, [rbx]
        or dil, dil
        jne branch_630
    branch_686:
        call mov_left
        call mov_left
        call mov_left
        call mov_left
        call mov_left
        call mov_left

        mov rdi, [rbx]
        or dil, dil
        je branch_733
    branch_693:
        call decrement
        call decrement
        call decrement
        call mov_left
        call decrement
        call decrement
        call decrement
        call decrement
        call decrement

        mov rdi, [rbx]
        or dil, dil
        je branch_728
    branch_703:
        call decrement

        mov rdi, [rbx]
        or dil, dil
        je branch_727
    branch_705:
        call decrement

        mov rdi, [rbx]
        or dil, dil
        je branch_726
    branch_707:
        call mov_left
        call decrement
        call mov_right
        call mov_right
        call increment
        call increment
        call increment
        call mov_left
        call increment
        call increment
        call increment
        call increment
        call increment
        call increment
        call increment

        mov rdi, [rbx]
        or dil, dil
        je branch_725
    branch_723:
        call decrement

        mov rdi, [rbx]
        or dil, dil
        jne branch_723
    branch_725:

        mov rdi, [rbx]
        or dil, dil
        jne branch_707
    branch_726:

        mov rdi, [rbx]
        or dil, dil
        jne branch_705
    branch_727:

        mov rdi, [rbx]
        or dil, dil
        jne branch_703
    branch_728:
        call mov_left
        call increment
        call mov_left
        call increment

        mov rdi, [rbx]
        or dil, dil
        jne branch_693
    branch_733:
        call mov_right

        mov rdi, [rbx]
        or dil, dil
        jne branch_366
    branch_735:
        call mov_right
        call mov_right

        mov rdi, [rbx]
        or dil, dil
        jne branch_198
    branch_738:

        mov rdi, [rbx]
        or dil, dil
        je branch_760
    branch_739:
        call write
        call write
        call write
        call write
        call read
        call write
        call write
        call write
        call read
        call read
        call write
        call write
        call decrement
        call write
        call decrement
        call write
        call write
        call decrement
        call write
        call write

        mov rdi, [rbx]
        or dil, dil
        jne branch_739
    branch_760:
        jmp exit
